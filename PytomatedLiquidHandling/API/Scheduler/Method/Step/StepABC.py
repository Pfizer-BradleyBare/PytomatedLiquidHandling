from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class StepABC(UniqueObjectABC):
    @abstractmethod
    def Execute(self, Simulate: bool):
        ...
