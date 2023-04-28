from ..DeckLocation import DeckLocation
from ..Labware import NonPipettableLabware
from .BaseLayoutItem import LayoutItem


class Lid(LayoutItem):
    def __init__(
        self,
        DeckLocationInstance: DeckLocation,
        Sequence: str,
        NonPipettableLabwareInstance: NonPipettableLabware,
    ):
        LayoutItem.__init__(
            self, DeckLocationInstance, Sequence, NonPipettableLabwareInstance
        )
