from dataclasses import dataclass, field
from enum import Enum

import networkx

from PytomatedLiquidHandling.API.Scheduler.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Step import StepABC, StepTracker, TaskABC


def StepGraphToTaskGraph(
    StepGraph: networkx.DiGraph, UniqueIdentifier: str
) -> networkx.DiGraph:
    TaskGraph = networkx.DiGraph()

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

            TaskList += Step.GetTasks(UniqueIdentifier)

            ChildrenNodes = list(StepGraph.successors(NodeName))

            if len(ChildrenNodes) > 1 or len(ChildrenNodes) == 0:
                break

            NodeName = ChildrenNodes[0]

        TaskList[-1].SchedulingSeparator = True
        # Last task is technically always a scheduling seperator. So let's set it

        Tasks: list[TaskABC] = list()

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

    Inner(list(networkx.topological_sort(StepGraph))[0], TaskGraph, None)
    return TaskGraph


@dataclass
class Method(UniqueObjectABC):
    StepGraphInstance: networkx.DiGraph
    Simulate: bool

    def GetTaskGraph(self) -> networkx.DiGraph:
        return StepGraphToTaskGraph(self.StepGraphInstance, str(self.UniqueIdentifier))
