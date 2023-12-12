from .Base import Layout
from .Numeric import Numeric
from typing import Literal

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class AlphaNumeric(Layout):
    Type: Literal["AlphaNumeric"] = "AlphaNumeric"

    def SortPositions(self, Positions: list[str | int]) -> list[str]:
        NumericAddressing = Numeric(
            Rows=self.Rows, Columns=self.Columns, Direction=self.Direction
        )

        return [
            self.GetPositionID(Pos)
            for Pos in NumericAddressing.SortPositions(Positions)
        ]

    def GroupPositionsColumnwise(self, Positions: list[str | int]) -> list[list[str]]:
        NumericAddressing = Numeric(
            Rows=self.Rows, Columns=self.Columns, Direction=self.Direction
        )

        return [
            [self.GetPositionID(Pos) for Pos in Group]
            for Group in NumericAddressing.GroupPositionsColumnwise(Positions)
        ]

    def GroupPositionsRowwise(self, Positions: list[str | int]) -> list[list[str]]:
        NumericAddressing = Numeric(
            Rows=self.Rows, Columns=self.Columns, Direction=self.Direction
        )

        return [
            [self.GetPositionID(Pos) for Pos in Group]
            for Group in NumericAddressing.GroupPositionsRowwise(Positions)
        ]

    def _GetColumnwisePositionID(self, Position: str) -> str:
        if Position.isalnum() and not Position.isalpha() and not Position.isdigit():
            return Position

        Pos = int(Position)

        NumberPortion = str(((Pos - 1) // self.Rows) + 1)

        CharacterPortion = chr(((Pos - 1) % self.Rows) + 65)

        return CharacterPortion + NumberPortion

    def _GetRowwisePositionID(self, Position: str) -> str:
        if Position.isalnum() and not Position.isalpha() and not Position.isdigit():
            return Position

        Pos = int(Position)

        NumberPortion = str(Pos % self.Columns)

        CharacterPortion = chr((Pos // self.Columns) + 65)

        return CharacterPortion + NumberPortion
