from ....Tools.AbstractClasses import UniqueObjectABC
from ...DeckLocation import DeckLocation
from ...Labware.BaseLabware import Labware


class LayoutItem(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        Sequence: str,
        LabwareInstance: Labware,
        DeckLocationInstance: DeckLocation,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.DeckLocationInstance: DeckLocation = DeckLocationInstance
        self.Sequence: str = Sequence
        self.LabwareInstance: Labware = LabwareInstance
