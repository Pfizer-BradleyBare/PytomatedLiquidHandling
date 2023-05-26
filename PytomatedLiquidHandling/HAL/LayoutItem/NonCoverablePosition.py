from ..DeckLocation.BaseDeckLocation import DeckLocationABC
from ..Labware import PipettableLabware
from .BaseLayoutItem import LayoutItemABC


class NonCoverablePosition(LayoutItemABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        PipettableLabwareInstance: PipettableLabware,
        DeckLocationInstance: DeckLocationABC,
    ):
        LayoutItemABC.__init__(
            self,
            UniqueIdentifier,
            Sequence,
            PipettableLabwareInstance,
            DeckLocationInstance,
        )
