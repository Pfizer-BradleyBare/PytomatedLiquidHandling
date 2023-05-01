from ..DeckLocation import DeckLocation
from ..Labware import NonPipettableLabware
from .BaseLayoutItem import LayoutItem


class Lid(LayoutItem):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        NonPipettableLabwareInstance: NonPipettableLabware,
        DeckLocationInstance: DeckLocation,
    ):
        LayoutItem.__init__(
            self,
            UniqueIdentifier,
            Sequence,
            NonPipettableLabwareInstance,
            DeckLocationInstance,
        )
