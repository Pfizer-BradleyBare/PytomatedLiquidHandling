from dataclasses import dataclass, field
from enum import Enum

import treelib

from PytomatedLiquidHandling.API.Scheduler.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Step import StepABC, StepTracker, TaskABC


@dataclass
class MethodABC(UniqueObjectABC):
    Simulate: bool
    StepTreeInstance: treelib.Tree

    StartingTaskList: list[TaskABC] = field(init=False)

    def __post_init__(self):
        StepPathways: list[StepTracker] = list()
        for StepPathway in self.StepTreeInstance.paths_to_leaves():
            StepTrackerInstance = StepTracker()

            for StepID in StepPathway:
                Node = self.StepTreeInstance.get_node(StepID)
                if not isinstance(Node, treelib.Node):
                    raise Exception("")
                # bad typing in treelib so we have to do this

                Step = Node.data
                if not isinstance(Step, StepABC):
                    raise Exception("")
                # bad typing in treelib so we have to do this

                if len(Node.fpointer) > 1:
                    Step.BranchStart = True
                else:
                    Step.BranchStart = False

                StepTrackerInstance.LoadSingle(Step)

            StepPathways.append(StepTrackerInstance)
        # Take the step tree and create discrete lists of step for each pathway.

        class DummyTask(TaskABC):
            def Execute(
                self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
            ):
                ...

        TaskPathways: list[list[TaskABC]] = list()
        for StepPathway in StepPathways:
            TaskPathway: list[TaskABC] = [
                DummyTask("Dummy", True, DummyTask.ExecutionWindows.Consecutive, [], 0)
            ]
            for Step in StepPathway.GetObjectsAsList():
                Tasks = Step.GetTasks()
                if len(Tasks) == 0:
                    continue
                if Step.BranchStart == True:
                    Tasks[-1].SchedulingSeparator = True
                # We must separate at the beginning of each branch to allow for efficient scheduling

                TaskPathway += Tasks

            TaskPathway[-1].SchedulingSeparator = True
            # Last task in pathway is always a separator

            TaskPathways.append(TaskPathway)
        # Convert to lists of tasks

        for TaskPathway in TaskPathways:
            TaskPathway.reverse()
            # Reverse because it makes things easier to move "up"

            ASAPTasks: list[TaskABC] = list()
            for Task in TaskPathway[:]:
                if Task.ExecutionWindow == Task.ExecutionWindows.AsSoonAsPossible:
                    ASAPTasks.append(Task)
                    TaskPathway.remove(Task)

                if Task.SchedulingSeparator == True:
                    InsertIndex = TaskPathway.index(Task)
                    for ASAPTask in ASAPTasks:
                        TaskPathway.insert(InsertIndex, ASAPTask)

            TaskPathway.reverse()
            # undo reverse

            TaskPathway.remove(TaskPathway[0])
            # remove the dummy ya dummy

        # reorganize tasks based on execution window setting

        SplitTaskPathways: list[list[list[TaskABC]]] = list()
        for TaskPathway in TaskPathways:
            SplitTaskPathway: list[list[TaskABC]] = list()
            SplitTasks: list[TaskABC] = list()
            for Task in TaskPathway:
                SplitTasks.append(Task)

                if Task.SchedulingSeparator == True:
                    SplitTaskPathway.append(SplitTasks)
                    SplitTasks = list()
            SplitTaskPathways.append(SplitTaskPathway)
        # split task lists into lists of lists of tasks. Each list is considered a sub method

        for SplitTaskPathway in SplitTaskPathways:
            SplitTaskPathway.reverse()
            PrevSplitTasks = None
            for SplitTasks in SplitTaskPathway:
                if not PrevSplitTasks is None:
                    SplitTasks[-1].QueueUponCompletion.append(PrevSplitTasks)
                PrevSplitTasks = SplitTasks
            SplitTaskPathway.reverse()
        # Go through each task sub list and connect them

        AllTasks: list[TaskABC] = list()
        for TaskPathway in TaskPathways:
            for Task in TaskPathway:
                AllTasks.append(Task)

        for BaseTask in AllTasks:
            QCollector = list()
            for Task in AllTasks:
                if BaseTask.UniqueIdentifier == Task.UniqueIdentifier:
                    QCollector += Task.QueueUponCompletion
            for Task in AllTasks:
                if BaseTask.UniqueIdentifier == Task.UniqueIdentifier:
                    Task.QueueUponCompletion = QCollector
        # combine the Q lists for each task because there could be repeats

        for TaskPathway in TaskPathways:
            for Task in TaskPathway:
                NewTaskList = list()
                for TasksList in Task.QueueUponCompletion:
                    if TasksList not in NewTaskList:
                        NewTaskList.append(TasksList)
                Task.QueueUponCompletion = NewTaskList
        # go back around and remove duplicates from the QueueUponCompletionList of Lists

        self.StartingTaskList = SplitTaskPathways[0][0]
        # jinkies
