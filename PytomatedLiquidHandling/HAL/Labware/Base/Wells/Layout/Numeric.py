from .Base import Layout
from typing import Literal


class Numeric(Layout):
    Type: Literal["Numeric"] = "Numeric"

    def _GetColumnwisePositionID(self, Position: str) -> str:
        if Position.isnumeric():
            return Position

        NumberPortion = "".join([c for c in Position if c.isdigit()])
        CharacterPortion = "".join([c for c in Position if c.isalpha()])

        Pos = (int(NumberPortion) - 1) * self.Rows

        Pos += ord(CharacterPortion) + 1 - 65  # ascii A

        return str(Pos)

    def _GetRowwisePositionID(self, Position: str) -> str:
        if Position.isnumeric():
            return Position

        NumberPortion = "".join([c for c in Position if c.isdigit()])
        CharacterPortion = "".join([c for c in Position if c.isalpha()])

        Pos = int(NumberPortion)

        Pos += (ord(CharacterPortion) - 65) * self.Columns  # ascii A

        return str(Pos)
