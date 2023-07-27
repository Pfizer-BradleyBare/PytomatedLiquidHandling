from dataclasses import dataclass

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import StepABC, TaskABC

from .Options import Options


@dataclass
class Step(StepABC):
    OptionsInstance: Options

    def GetTasks(self, MethodName: str, Simulate: bool) -> list[TaskABC]:
        ...
