from abc import abstractmethod
from .....Tools.AbstractClasses import UniqueObjectABC
from dataclasses import dataclass


@dataclass
class StepABC(UniqueObjectABC):
    @abstractmethod
    def Execute(self, Simulate: bool):
        ...
