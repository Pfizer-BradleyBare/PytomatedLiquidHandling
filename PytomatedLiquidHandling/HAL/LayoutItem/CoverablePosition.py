from ..DeckLocation.BaseDeckLocation import DeckLocationABC
from ..Labware import PipettableLabware
from .BaseLayoutItem import LayoutItemABC
from .Lid import Lid


class CoverablePosition(LayoutItemABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        PipettableLabwareInstance: PipettableLabware,
        DeckLocationInstance: DeckLocationABC,
        LidInstance: Lid,
    ):
        LayoutItemABC.__init__(
            self,
            UniqueIdentifier,
            Sequence,
            PipettableLabwareInstance,
            DeckLocationInstance,
        )
        self.LidInstance: Lid = LidInstance
