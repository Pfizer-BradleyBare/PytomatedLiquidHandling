from typing import Generator

from PytomatedLiquidHandling.API.Scheduler.Method import Step
from PytomatedLiquidHandling.API.Scheduler.Method.Step.TaskABC import TaskABC
from PytomatedLiquidHandling.API.Scheduler.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger


class PipetteTask(Step.TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


class LiquidTransfer(Step.StepABC):
    def GetTasks(self, i) -> list[TaskABC]:
        return [
            PipetteTask(
                str(self.UniqueIdentifier) + "Pipette 1" + i,
                PipetteTask.ExecutionWindows.Consecutive,
                False,
                15,
                ["Hamilton"],
            ),
            PipetteTask(
                str(self.UniqueIdentifier) + "Pipette 2" + i,
                PipetteTask.ExecutionWindows.Consecutive,
                False,
                15,
                ["Hamilton"],
            ),
        ]
