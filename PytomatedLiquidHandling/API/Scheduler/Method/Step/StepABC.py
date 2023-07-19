from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .TaskABC import TaskABC


@dataclass
class StepABC(UniqueObjectABC):
    BranchStart: bool = field(init=False, default=False)

    @abstractmethod
    def GetTasks(self) -> list[TaskABC]:
        ...
