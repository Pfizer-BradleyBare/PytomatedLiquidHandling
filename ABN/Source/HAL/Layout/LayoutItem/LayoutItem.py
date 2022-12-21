from ...DeckLocation import DeckLocation
from ...Labware import Labware


class LayoutItem:
    def __init__(
        self,
        Sequence: str,
        DeckLocationInstance: DeckLocation,
        LabwareInstance: Labware,
    ):
        self.Sequence: str = Sequence
        self.LabwareInstance: Labware = LabwareInstance
        self.DeckLocationInstance: DeckLocation = DeckLocationInstance

    def GetSequence(self) -> str:
        return self.Sequence

    def GetLabware(self) -> Labware:
        return self.LabwareInstance

    def GetDeckLocation(self) -> DeckLocation:
        return self.DeckLocationInstance
