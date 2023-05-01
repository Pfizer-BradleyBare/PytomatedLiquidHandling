from ....Tools.AbstractClasses import UniqueObjectABC
from ...DeckLocation import DeckLocation
from ...Labware.BaseLabware import Labware


class LayoutItem(UniqueObjectABC):
    def __init__(
        self,
        DeckLocationInstance: DeckLocation,
        Sequence: str,
        LabwareInstance: Labware,
    ):
        self.DeckLocationInstance: DeckLocation = DeckLocationInstance
        self.Sequence: str = Sequence
        self.LabwareInstance: Labware = LabwareInstance

    def GetUniqueIdentifier(self) -> str:
        return self.Sequence
