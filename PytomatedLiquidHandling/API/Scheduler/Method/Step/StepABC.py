from abc import abstractmethod
from dataclasses import dataclass
from typing import Generator

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .TaskABC import TaskABC


@dataclass
class StepABC(UniqueObjectABC):
    @abstractmethod
    def GetTasks(self) -> list[TaskABC]:
        ...
