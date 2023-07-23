from dataclasses import dataclass

from PytomatedLiquidHandling.API.Scheduler.Method.Step.TaskABC import TaskABC
from PytomatedLiquidHandling.API.Scheduler.Method.Step import StepABC
from PytomatedLiquidHandling.API.Scheduler.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger


@dataclass
class StartHeater(TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


@dataclass
class Transport(TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


@dataclass
class Wait(TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


@dataclass
class StopHeater(TaskABC):
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        return super().Execute(LoggerInstance, OrchastratorInstance)


@dataclass
class Incubate(StepABC):
    def GetTasks(self, i) -> list[TaskABC]:
        return [
            StartHeater(
                str(self.UniqueIdentifier) + "1",
                StartHeater.ExecutionWindows.AsSoonAsPossible,
                False,
                15,
                [],
            ),
            Transport(
                str(self.UniqueIdentifier) + "2",
                StartHeater.ExecutionWindows.Consecutive,
                False,
                15,
                [],
            ),
            Wait(
                str(self.UniqueIdentifier) + "3",
                StartHeater.ExecutionWindows.Consecutive,
                True,
                15,
                [],
            ),
            Transport(
                str(self.UniqueIdentifier) + "4",
                StartHeater.ExecutionWindows.Consecutive,
                False,
                15,
                [],
            ),
            StopHeater(
                str(self.UniqueIdentifier) + "5",
                StartHeater.ExecutionWindows.Consecutive,
                False,
                15,
                [],
            ),
        ]
