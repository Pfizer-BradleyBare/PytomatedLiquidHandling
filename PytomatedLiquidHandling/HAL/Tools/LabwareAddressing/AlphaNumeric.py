from dataclasses import dataclass

from .Base import InvalidPositionError, LabwareAddressing, LabwarePosition


class AlphaNumericPosition(LabwarePosition):
    def __init__(self, Position: str):
        if not Position.isalnum() and Position.isalpha() and Position.isdigit():
            raise InvalidPositionError(
                "Must contain both numbers and letters. Ex: A1, B12, 10H"
            )
        LabwarePosition.__init__(self, Position)


@dataclass
class AlphaNumericAddressing(LabwareAddressing):
    def GetColumnwisePosition(self, Position: LabwarePosition) -> str:
        if (
            Position.Value.isalnum()
            and not Position.Value.isalpha()
            and not Position.Value.isdigit()
        ):
            return Position.Value

        Pos = int(Position.Value)

        NumberPortion = str(((Pos - 1) // self.Rows) + 1)

        CharacterPortion = chr(((Pos - 1) % self.Rows) + 65)

        return CharacterPortion + NumberPortion

    def GetRowwisePosition(self, Position: LabwarePosition) -> str:
        if (
            Position.Value.isalnum()
            and not Position.Value.isalpha()
            and not Position.Value.isdigit()
        ):
            return Position.Value

        Pos = int(Position.Value)

        NumberPortion = str(Pos % self.Columns)

        CharacterPortion = chr((Pos // self.Columns) + 65)

        return CharacterPortion + NumberPortion
