from dataclasses import dataclass, field
from enum import Enum

import networkx

from PytomatedLiquidHandling.API.Tools.Container import ContainerTracker
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ..Orchastrator import Orchastrator
from .Step import StepABC, TaskABC


@dataclass
class Method(UniqueObjectABC):
    StepGraphInstance: networkx.DiGraph
    Simulate: bool

    ContainerTrackerInstance: ContainerTracker = field(
        init=False, default_factory=ContainerTracker
    )

    def GetTaskGraph(self, OrchastratorInstance: Orchastrator) -> networkx.DiGraph:
        TaskGraph = networkx.DiGraph()

        StepGraph = self.StepGraphInstance

        def Inner(
            NodeName: str,
            TaskGraph: networkx.DiGraph,
            ParentNode: str | None,
        ):
            StartingNodeName = NodeName

            ChildrenNodes = list()

            TaskList: list[TaskABC] = list()
            StepList: list[StepABC] = list()

            Tasks: list[TaskABC] = list()

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

                TaskList += [
                    TaskClass(
                        str(self.UniqueIdentifier)
                        + ":"
                        + str(Step.UniqueIdentifier)
                        + ":"
                        + str(Count)
                        + ":"
                        + TaskClass.__name__,
                        self.Simulate,
                        Tasks,
                        OrchastratorInstance,
                    )
                    for Count, TaskClass in enumerate(Step.TaskClasses)
                ]

                ChildrenNodes = list(StepGraph.successors(NodeName))

                if len(ChildrenNodes) > 1 or len(ChildrenNodes) == 0:
                    break

                NodeName = ChildrenNodes[0]

            TaskList[-1].SchedulingSeparator = True
            # Last task is always a scheduling separator.

            CombinedNodeName = ""

            for Task in TaskList:
                if Task.ExecutionWindow == Task.ExecutionWindows.Consecutive:
                    Tasks.append(Task)
                elif Task.ExecutionWindow == Task.ExecutionWindows.AsSoonAsPossible:
                    Tasks.insert(0, Task)

                if Task.SchedulingSeparator == True:
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
