from abc import ABC, abstractmethod
from dataclasses import dataclass


class InvalidPositionError(ValueError):
    ...


class LabwarePosition(ABC):
    @abstractmethod
    def __init__(self, Position: str | int):
        self.Value: str = str(Position)


@dataclass
class LabwareAddressing(ABC):
    Rows: int = 8
    Columns: int = 12

    @abstractmethod
    def GetColumnwisePosition(self, Position: LabwarePosition) -> str:
        ...

    @abstractmethod
    def GetRowwisePosition(self, Position: LabwarePosition) -> str:
        ...
