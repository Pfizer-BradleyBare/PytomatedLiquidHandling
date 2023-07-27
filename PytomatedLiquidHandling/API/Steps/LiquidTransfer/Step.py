from dataclasses import dataclass

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import StepABC, TaskABC

from .OptionsTracker import OptionsTracker


@dataclass
class Step(StepABC):
    OptionsTrackerInstance: OptionsTracker

    def GetTasks(self, MethodName: str, Simulate: bool) -> list[TaskABC]:
        ...
