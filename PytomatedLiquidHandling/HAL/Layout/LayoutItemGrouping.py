from ...Tools.AbstractClasses import UniqueObjectABC
from ..DeckLocation import DeckLocation
from ..Labware import Labware
from .LayoutItem.LayoutItem import LayoutItem


class LayoutItemGrouping(UniqueObjectABC):
    def __init__(
        self,
        PlateLayoutItemInstance: LayoutItem,
        LidLayoutItemInstance: LayoutItem | None,
    ):
        self.Name: str = (
            PlateLayoutItemInstance.DeckLocationInstance.GetName()
            + " -> "
            + PlateLayoutItemInstance.LabwareInstance.GetName()
        )
        self.PlateLayoutItemInstance: LayoutItem = PlateLayoutItemInstance
        self.LidLayoutItemInstance: LayoutItem | None = LidLayoutItemInstance

    def GetName(self) -> str:
        return self.Name

    def HasLid(self) -> bool:
        return self.LidLayoutItemInstance != None

    def GetDeckLocation(self) -> DeckLocation:
        return self.PlateLayoutItemInstance.DeckLocationInstance

    def GetLabware(self) -> Labware:
        return self.PlateLayoutItemInstance.LabwareInstance
