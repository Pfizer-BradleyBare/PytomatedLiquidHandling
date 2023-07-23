from dataclasses import dataclass, field
from enum import Enum

import networkx

from PytomatedLiquidHandling.API.Scheduler.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Step import StepABC, StepTracker, TaskABC


def StepTreeToTaskTree(
    StepTree: networkx.DiGraph, UniqueIdentifier: str
) -> networkx.DiGraph:
    TaskTree = networkx.DiGraph()

    def Inner(
        NodeName: str,
        TaskTree: networkx.DiGraph,
        ParentNode: str | None,
    ):
        StartingNodeName = NodeName

        ChildrenNodes = list()

        TaskList: list[TaskABC] = list()
        StepList: list[StepABC] = list()

        while True:
            Node = StepTree.nodes[NodeName]

            if (
                len(list(StepTree.predecessors(NodeName))) > 1
                and NodeName != StartingNodeName
            ):
                break
            # Since this is a method graph we need to check if a node has more than one parent (Synchronization).
            # If so we need to split those nodes.
            # If the nodename is equal to the startingnodename then that means we have started on the node with more than 1 parent

            Step: StepABC = Node["Step"]
            StepList.append(Step)

            TaskList += Step.GetTasks(UniqueIdentifier)

            ChildrenNodes = list(StepTree.successors(NodeName))

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

                TaskTree.add_node(CombinedNodeName, Steps=StepList, Tasks=Tasks)
                if ParentNode is not None:
                    TaskTree.add_edge(ParentNode, CombinedNodeName)
                    ParentNode = CombinedNodeName

                Tasks = list()
        # task reordering / splitting. TODO refactor

        for ChildNode in ChildrenNodes:
            Inner(
                ChildNode,
                TaskTree,
                CombinedNodeName,
            )

    Inner(list(networkx.topological_sort(StepTree))[0], TaskTree, None)
    return TaskTree


@dataclass
class Method(UniqueObjectABC):
    StepTreeInstance: networkx.DiGraph
    Simulate: bool

    def GetTaskTree(self) -> networkx.DiGraph:
        return StepTreeToTaskTree(self.StepTreeInstance, str(self.UniqueIdentifier))
