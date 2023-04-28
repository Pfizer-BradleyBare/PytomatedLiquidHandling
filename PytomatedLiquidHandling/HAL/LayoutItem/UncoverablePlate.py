from ..DeckLocation import DeckLocation
from ..Labware import PipettableLabware
from .BaseLayoutItem import LayoutItem


class UncoverablePlate(LayoutItem):
    def __init__(
        self,
        DeckLocationInstance: DeckLocation,
        Sequence: str,
        PipettableLabwareInstance: PipettableLabware,
    ):
        LayoutItem.__init__(
            self, DeckLocationInstance, Sequence, PipettableLabwareInstance
        )
