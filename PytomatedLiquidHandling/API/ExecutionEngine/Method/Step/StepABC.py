from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .TaskABC import TaskABC


@dataclass
class StepABC(UniqueObjectABC):
    @abstractmethod
    def GetTasks(self, MethodName: str, Simulate: bool) -> list[TaskABC]:
        ...
