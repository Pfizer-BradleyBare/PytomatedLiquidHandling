from abc import ABC, abstractmethod
from pydantic import dataclasses

from enum import Enum


class InvalidPositionError(ValueError):
    ...


@dataclasses.dataclass(kw_only=True)
class Layout(ABC):
    class Sorting(Enum):
        Columnwise = "Columnwise"
        Rowwise = "Rowwise"

    Rows: int = 8
    Columns: int = 12
    Direction: Sorting = Sorting.Columnwise

    def GetPositionID(self, Position: str | int) -> str:
        if isinstance(Position, int):
            Position = str(Position)

        Fail = False
        if not Position.isalnum() and Position.isalpha() and Position.isdigit():
            Fail = True
        elif not Position.isdigit():
            Fail = True

        if Fail == True:
            raise InvalidPositionError(
                "Position can be either alphanumeric or numeric.\nAlphanumeric must contain both numbers and letters. Ex: A1, B12, 10H.\nNumeric must only contain digits. Ex: 1 13 95"
            )

        if self.Direction == Layout.Sorting.Columnwise:
            return self._GetColumnwisePositionID(Position)
        else:
            return self._GetRowwisePositionID(Position)

    @abstractmethod
    def SortPositions(self, Positions: list[str | int], key=lambda x: x) -> list[str]:
        ...

    @abstractmethod
    def GroupPositionsColumnwise(
        self, Positions: list[str | int], key=lambda x: x
    ) -> list[list[str]]:
        ...

    @abstractmethod
    def GroupPositionsRowwise(
        self, Positions: list[str | int], key=lambda x: x
    ) -> list[list[str]]:
        ...

    @abstractmethod
    def _GetColumnwisePositionID(self, Position: str) -> str:
        ...

    @abstractmethod
    def _GetRowwisePositionID(self, Position: str) -> str:
        ...
