from ..DeckLocation import DeckLocation
from ..Labware import PipettableLabware
from .BaseLayoutItem import LayoutItem
from .Lid import Lid


class CoverablePosition(LayoutItem):
    def __init__(
        self,
        DeckLocationInstance: DeckLocation,
        Sequence: str,
        PipettableLabwareInstance: PipettableLabware,
        LidInstance: Lid,
    ):
        LayoutItem.__init__(
            self, DeckLocationInstance, Sequence, PipettableLabwareInstance
        )
        self.LidInstance: Lid = LidInstance
