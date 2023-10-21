from .Base import Layout
from typing import Literal


class AlphaNumeric(Layout):
    Type: Literal["AlphaNumeric"] = "AlphaNumeric"

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
