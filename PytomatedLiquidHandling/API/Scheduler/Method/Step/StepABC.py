from abc import abstractmethod
from dataclasses import dataclass
from typing import Generator

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from .SubStepABC import SubStepABC


@dataclass
class StepABC(UniqueObjectABC):
    @abstractmethod
    def GetSubSteps(self) -> Generator[SubStepABC, None, None]:
        ...
