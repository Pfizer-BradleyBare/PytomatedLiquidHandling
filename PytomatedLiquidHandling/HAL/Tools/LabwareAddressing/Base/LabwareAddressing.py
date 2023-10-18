from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class InvalidPositionError(ValueError):
    ...


class LabwarePosition(ABC):
    @abstractmethod
    def __init__(self, Position: str | int):
        self.Value: str = str(Position)


class Sorting(Enum):
    Columnwise = "Columnwise"
    Rowwise = "Rowwise"


@dataclass
class LabwareAddressing(ABC):
    Rows: int = 8
    Columns: int = 12
    SortDirection: Sorting = Sorting.Columnwise

    def GetPosition(self, Position: LabwarePosition) -> str:
        if self.SortDirection == Sorting.Columnwise:
            return self._GetColumnwisePosition(Position)
        else:
            return self._GetRowwisePosition(Position)

    @abstractmethod
    def _GetColumnwisePosition(self, Position: LabwarePosition) -> str:
        ...

    @abstractmethod
    def _GetRowwisePosition(self, Position: LabwarePosition) -> str:
        ...
