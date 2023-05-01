from ..DeckLocation import DeckLocation
from ..Labware import PipettableLabware
from .BaseLayoutItem import LayoutItem


class UncoverablePosition(LayoutItem):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        PipettableLabwareInstance: PipettableLabware,
        DeckLocationInstance: DeckLocation,
    ):
        LayoutItem.__init__(
            self,
            UniqueIdentifier,
            Sequence,
            PipettableLabwareInstance,
            DeckLocationInstance,
        )
