from ..DeckLocation import DeckLocation
from ..Labware import Labware
from .BaseLayoutItem import LayoutItem
from .Lid import Lid


class CoverablePosition(LayoutItem):
    def __init__(
        self,
        DeckLocationInstance: DeckLocation,
        Sequence: str,
        LabwareInstance: Labware,
        LidInstance: Lid,
    ):
        LayoutItem.__init__(self, DeckLocationInstance, Sequence, LabwareInstance)
        self.LidInstance: Lid = LidInstance
