from ..Labware import Labware
from ..Layout import LayoutItem
from ...AbstractClasses import ObjectABC


class Lid(ObjectABC):
    def __init__(
        self,
        Name: str,
        LidLayoutItem: LayoutItem,
        SupportedLabware: list[Labware],
    ):
        self.Name: str = Name
        self.LidLayoutItem: LayoutItem = LidLayoutItem
        self.SupportedLabware: list[Labware] = SupportedLabware

    def GetName(self) -> str:
        return self.Name

    def GetLidLayoutItem(self) -> LayoutItem:
        return self.LidLayoutItem

    def GetSupportedLabware(self) -> list[Labware]:
        return self.SupportedLabware
