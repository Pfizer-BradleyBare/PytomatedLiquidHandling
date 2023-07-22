from dataclasses import dataclass, field
from enum import Enum

import treelib

from PytomatedLiquidHandling.API.Scheduler.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Step import StepABC, StepTracker, TaskABC


def StepTreeToTaskTree(StepTree: treelib.Tree, UniqueIdentifier: str) -> treelib.Tree:
    TaskTree = treelib.Tree()

    def Inner(
        StepTree: treelib.Tree,
        TaskTree: treelib.Tree,
        NodeParent: str | None,
        NodeCounter: int,
    ) -> int:
        TaskList: list[TaskABC] = list()
        ChildrenNodes = list()

        for Node in StepTree.all_nodes():
            if not isinstance(Node, treelib.Node):
                raise Exception("")
            # bad typing in treelib so we have to do this

            Step = Node.data
            if not isinstance(Step, StepABC):
                raise Exception("")
            # bad typing in treelib so we have to do this

            TaskList += Step.GetTasks(UniqueIdentifier)

            ChildrenNodes = Node.successors(StepTree.identifier)

            if len(ChildrenNodes) > 1:
                break

        Tasks: list[TaskABC] = list()

        for Task in TaskList:
            if Task.ExecutionWindow == Task.ExecutionWindows.Consecutive:
                Tasks.append(Task)
            elif Task.ExecutionWindow == Task.ExecutionWindows.AsSoonAsPossible:
                Tasks.insert(0, Task)

            if Task.SchedulingSeparator == True:
                ParentNodeName = str(NodeCounter)
                TaskTree.create_node(
                    identifier=ParentNodeName, parent=NodeParent, data=Tasks
                )
                NodeCounter += 1
                NodeParent = ParentNodeName
                Tasks = list()
        # task reordering / splitting. TODO refactor

        if len(Tasks) != 0:
            ParentNodeName = str(NodeCounter)
            TaskTree.create_node(
                identifier=ParentNodeName, parent=NodeParent, data=Tasks
            )
            NodeCounter += 1
            NodeParent = ParentNodeName

        if len(ChildrenNodes) > 1:
            for ChildNode in ChildrenNodes:
                NodeCounter += Inner(
                    StepTree.subtree(ChildNode),
                    TaskTree,
                    NodeParent,
                    NodeCounter,
                )
        return NodeCounter

    Inner(StepTree, TaskTree, None, 0)
    return TaskTree


@dataclass
class Method(UniqueObjectABC):
    StepTreeInstance: treelib.Tree
    Simulate: bool

    def GetTaskTree(self) -> treelib.Tree:
        return StepTreeToTaskTree(self.StepTreeInstance, str(self.UniqueIdentifier))
