from typing import Generator

from PytomatedLiquidHandling.API.Scheduler.Method import Step
from PytomatedLiquidHandling.API.Scheduler.Method.Step.TaskABC import TaskABC
from PytomatedLiquidHandling.API.Scheduler.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger


class StartHeater(Step.TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


class Transport(Step.TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


class Wait(Step.TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


class StopHeater(Step.TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


class Incubate(Step.StepABC):
    def GetTasks(self) -> list[TaskABC]:
        return [
            StartHeater(
                str(self.UniqueIdentifier) + "1",
                False,
                StartHeater.ExecutionWindows.AsSoonAsPossible,
                [],
                15,
            ),
            Transport(
                str(self.UniqueIdentifier) + "2",
                False,
                Transport.ExecutionWindows.Consecutive,
                [],
                15,
            ),
            Wait(
                str(self.UniqueIdentifier) + "3",
                True,
                Wait.ExecutionWindows.Consecutive,
                [],
                15,
            ),
            Transport(
                str(self.UniqueIdentifier) + "4",
                False,
                Transport.ExecutionWindows.Consecutive,
                [],
                15,
            ),
            StopHeater(
                str(self.UniqueIdentifier) + "5",
                False,
                StopHeater.ExecutionWindows.Consecutive,
                [],
                15,
            ),
        ]
