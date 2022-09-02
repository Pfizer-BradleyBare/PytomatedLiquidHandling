from ..DeckLocation import DeckLocation
from ..Labware import Labware
from ...AbstractClasses import ObjectABC


class LayoutItemLidTracker:
    def __init__(self, HasLid: bool):
        self.HasLid: bool = HasLid

    def HasLidSequence(self) -> bool:
        return self.HasLid


class LayoutItem(ObjectABC, LayoutItemLidTracker):
    def __init__(
        self,
        Sequence: str,
        DeckLocationInstance: DeckLocation,
        LabwareInstance: Labware,
    ):
        LayoutItemLidTracker.__init__(self, False)
        self.Sequence: str = Sequence
        self.LabwareInstance: Labware = LabwareInstance
        self.DeckLocationInstance: DeckLocation = DeckLocationInstance

    def GetName(self) -> str:
        return self.Sequence

    def GetSequence(self) -> str:
        return self.Sequence

    def GetLabware(self) -> Labware:
        return self.LabwareInstance

    def GetDeckLocation(self) -> DeckLocation:
        return self.DeckLocationInstance


class CoveredLayoutItem(LayoutItem):
    def __init__(
        self,
        Sequence: str,
        LidSequence: str,
        DeckLocationInstance: DeckLocation,
        LabwareInstance: Labware,
    ):
        LayoutItem.__init__(self, Sequence, DeckLocationInstance, LabwareInstance)
        LayoutItemLidTracker.__init__(self, True)

        self.LidSequence: str = LidSequence

    def GetLidSequence(self) -> str:
        return self.LidSequence
