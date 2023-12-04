from .Base import Layout
from typing import Literal


class Numeric(Layout):
    Type: Literal["Numeric"] = "Numeric"

    def SortPositions(self, Positions: list[str | int]) -> list[str]:
        return sorted([self.GetPositionID(Pos) for Pos in Positions])

    def GroupPositionsColumnwise(self, Positions: list[str | int]) -> list[list[str]]:
        SortedPositions = self.SortPositions(Positions)

        Groups = [[] for _ in range(self.Columns)]
        for Pos in SortedPositions:
            Groups[int((int(Pos) - 1) / self.Rows)].append(Pos)

        return [Group for Group in Groups if len(Group) != 0]

    def GroupPositionsRowwise(self, Positions: list[str | int]) -> list[list[str]]:
        SortedPositions = self.SortPositions(Positions)

        Groups = [[] for _ in range(self.Rows)]
        for Pos in SortedPositions:
            Groups[int((int(Pos) - 1) / self.Columns)].append(Pos)

        return [Group for Group in Groups if len(Group) != 0]

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
