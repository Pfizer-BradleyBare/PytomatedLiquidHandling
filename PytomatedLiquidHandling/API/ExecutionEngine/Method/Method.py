from dataclasses import dataclass, field
from enum import Enum

import networkx

from PytomatedLiquidHandling.API.Tools.Container import ContainerTracker
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .Step import StepABC, TaskABC


@dataclass
class Method(UniqueObjectABC):
    StepGraphInstance: networkx.DiGraph
    Simulate: bool

    ContainerTrackerInstance: ContainerTracker = field(
        init=False, default_factory=ContainerTracker
    )

    def GetTaskGraph(self) -> networkx.DiGraph:
        TaskGraph = networkx.DiGraph()

        StepGraph = self.StepGraphInstance
        UniqueIdentifier = str(self.UniqueIdentifier)

        def Inner(
            NodeName: str,
            TaskGraph: networkx.DiGraph,
            ParentNode: str | None,
        ):
            StartingNodeName = NodeName

            ChildrenNodes = list()

            TaskList: list[TaskABC] = list()
            StepList: list[StepABC] = list()

            while True:
                Node = StepGraph.nodes[NodeName]

                if (
                    len(list(StepGraph.predecessors(NodeName))) > 1
                    and NodeName != StartingNodeName
                ):
                    break
                # Since this is a method graph we need to check if a node has more than one parent (Synchronization).
                # If so we need to split those nodes.
                # If the nodename is equal to the startingnodename then that means we have started on the node with more than 1 parent

                Step: StepABC = Node["Step"]
                StepList.append(Step)

                TaskList += Step.GetTasks(UniqueIdentifier, self.Simulate)

                ChildrenNodes = list(StepGraph.successors(NodeName))

                if len(ChildrenNodes) > 1 or len(ChildrenNodes) == 0:
                    break

                NodeName = ChildrenNodes[0]

            Tasks: list[TaskABC] = list()

            CombinedNodeName = ""

            LastTaskID = TaskList[-1].UniqueIdentifier

            for Task in TaskList:
                if Task.GetExecutionWindow() == Task.ExecutionWindows.Consecutive:
                    Tasks.append(Task)
                elif (
                    Task.GetExecutionWindow() == Task.ExecutionWindows.AsSoonAsPossible
                ):
                    Tasks.insert(0, Task)

                if (
                    Task.IsSchedulingSeparator() == True
                    or Task.UniqueIdentifier == LastTaskID
                ):
                    CombinedNodeName = "|".join(
                        [str(Task.UniqueIdentifier) for Task in Tasks]
                    )

                    TaskGraph.add_node(CombinedNodeName, Steps=StepList, Tasks=Tasks)
                    if ParentNode is not None:
                        TaskGraph.add_edge(ParentNode, CombinedNodeName)

                    ParentNode = CombinedNodeName

                    Tasks = list()
            # task reordering / splitting. TODO refactor

            for ChildNode in ChildrenNodes:
                Inner(
                    ChildNode,
                    TaskGraph,
                    CombinedNodeName,
                )

        Inner(
            list(networkx.topological_sort(StepGraph))[0],  # type:ignore
            TaskGraph,
            None,
        )
        return TaskGraph
