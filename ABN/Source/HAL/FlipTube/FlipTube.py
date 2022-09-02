from ..Labware import Labware
from ...AbstractClasses import ObjectABC


class FlipTube(ObjectABC):
    def __init__(self, Name: str, Sequence: str, SupportedLabware: list[Labware]):
        self.Name: str = Name
        self.Sequence: str = Sequence
        self.SupportedLabware: list[Labware] = SupportedLabware

    def GetName(self) -> str:
        return self.Name

    def GetSequence(self) -> str:
        return self.Sequence

    def GetSupportedLabware(self) -> list[Labware]:
        return self.SupportedLabware
