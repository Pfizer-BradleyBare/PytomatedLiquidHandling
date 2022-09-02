from ...AbstractClasses import TrackerABC
from ..Labware import LabwareTracker
from ..DeckLocation import DeckLocationTracker
from .Lid import Lid


class LidTracker(TrackerABC):
    def __init__(
        self,
        LabwareTrackerInstance: LabwareTracker,
        DeckLocationTrackerInstance: DeckLocationTracker,
    ):
        self.Collection: dict[str, Lid] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )

    def LoadManual(self, LidInstance: Lid):
        Name = LidInstance.GetName()

        if Name in self.Collection:
            raise Exception("Lid Already Exists")

        self.Collection[Name] = LidInstance

    def GetLoadedObjectsAsDictionary(self) -> dict[str, Lid]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[Lid]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> Lid:
        return self.Collection[Name]
