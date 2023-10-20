from abc import ABC, abstractmethod
from pydantic import BaseModel
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


class Addressing(BaseModel, ABC):
    Rows: int = 8
    Columns: int = 12
    Direction: Sorting = Sorting.Columnwise

    def GetPosition(self, Position: LabwarePosition) -> str:
        if self.Direction == Sorting.Columnwise:
            return self._GetColumnwisePosition(Position)
        else:
            return self._GetRowwisePosition(Position)

    @abstractmethod
    def _GetColumnwisePosition(self, Position: LabwarePosition) -> str:
        ...

    @abstractmethod
    def _GetRowwisePosition(self, Position: LabwarePosition) -> str:
        ...
