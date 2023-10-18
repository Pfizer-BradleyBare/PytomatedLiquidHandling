from dataclasses import dataclass

from .Base import InvalidPositionError, LabwareAddressing, LabwarePosition


class NumericPosition(LabwarePosition):
    def __init__(self, Position: str | int):
        Position = str(Position)
        if not Position.isdigit():
            raise InvalidPositionError("Must only contain digits. Ex. 1 13 95")
        LabwarePosition.__init__(self, Position)


@dataclass
class NumericAddressing(LabwareAddressing):
    def _GetColumnwisePosition(self, Position: LabwarePosition) -> str:
        if Position.Value.isnumeric():
            return Position.Value

        NumberPortion = "".join([c for c in Position.Value if c.isdigit()])
        CharacterPortion = "".join([c for c in Position.Value if c.isalpha()])

        Pos = (int(NumberPortion) - 1) * self.Rows

        Pos += ord(CharacterPortion) + 1 - 65  # ascii A

        return str(Pos)

    def _GetRowwisePosition(self, Position: LabwarePosition) -> str:
        if Position.Value.isnumeric():
            return Position.Value

        NumberPortion = "".join([c for c in Position.Value if c.isdigit()])
        CharacterPortion = "".join([c for c in Position.Value if c.isalpha()])

        Pos = int(NumberPortion)

        Pos += (ord(CharacterPortion) - 65) * self.Columns  # ascii A

        return str(Pos)
