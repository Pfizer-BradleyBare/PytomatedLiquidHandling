from ..DeckLocation.BaseDeckLocation import DeckLocationABC
from ..Labware import NonPipettableLabware
from .BaseLayoutItem import LayoutItemABC


class Lid(LayoutItemABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        NonPipettableLabwareInstance: NonPipettableLabware,
        DeckLocationInstance: DeckLocationABC,
    ):
        LayoutItemABC.__init__(
            self,
            UniqueIdentifier,
            Sequence,
            NonPipettableLabwareInstance,
            DeckLocationInstance,
        )
