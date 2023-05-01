from ..DeckLocation import DeckLocation
from ..Labware import PipettableLabware
from .BaseLayoutItem import LayoutItem
from .Lid import Lid


class CoverablePosition(LayoutItem):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        PipettableLabwareInstance: PipettableLabware,
        DeckLocationInstance: DeckLocation,
        LidInstance: Lid,
    ):
        LayoutItem.__init__(
            self,
            UniqueIdentifier,
            Sequence,
            PipettableLabwareInstance,
            DeckLocationInstance,
        )
        self.LidInstance: Lid = LidInstance
