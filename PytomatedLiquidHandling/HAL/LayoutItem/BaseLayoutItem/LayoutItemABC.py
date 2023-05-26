from ....Tools.AbstractClasses import UniqueObjectABC
from ...DeckLocation.BaseDeckLocation import DeckLocationABC
from ...Labware.BaseLabware import LabwareABC


class LayoutItemABC(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        LabwareInstance: LabwareABC,
        DeckLocationInstance: DeckLocationABC,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.DeckLocationInstance: DeckLocationABC = DeckLocationInstance
        self.Sequence: str = Sequence
        self.LabwareInstance: LabwareABC = LabwareInstance
