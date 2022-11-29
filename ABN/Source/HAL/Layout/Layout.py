from ...Tools.AbstractClasses import ObjectABC
from ..DeckLocation import DeckLocation
from ..Labware import Labware


class LayoutItem(ObjectABC):
    def __init__(
        self,
        Sequence: str,
        LidSequence: str | None,
        DeckLocationInstance: DeckLocation,
        LabwareInstance: Labware,
    ):
        self.Sequence: str = Sequence
        self.LidSequence: str | None = LidSequence
        self.LabwareInstance: Labware = LabwareInstance
        self.DeckLocationInstance: DeckLocation = DeckLocationInstance

    def GetName(self) -> str:
        return self.Sequence

    def GetSequence(self) -> str:
        return self.Sequence

    def GetLabware(self) -> Labware:
        return self.LabwareInstance

    def GetDeckLocation(self) -> DeckLocation:
        return self.DeckLocationInstance

    def HasLid(self) -> bool:
        return self.LidSequence is not None

    def GetLidSequence(self) -> str:
        if self.LidSequence is None:
            raise Exception(
                "Layout Item does not have a lid? Did you check HasLid first?"
            )

        return self.LidSequence
