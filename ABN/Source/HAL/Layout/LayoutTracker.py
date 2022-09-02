from ...AbstractClasses import TrackerABC
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .Layout import LayoutItem


class LayoutTracker(TrackerABC):
    def __init__(
        self,
        DeckLocationTrackerInstance: DeckLocationTracker,
        LabwareTrackerInstance: LabwareTracker,
    ):
        self.Collection: dict[str, LayoutItem] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )

    def LoadManual(self, LayoutItemInstance: LayoutItem):
        Name = LayoutItemInstance.GetName()

        if Name in self.Collection:
            raise Exception("Layout Item Already Exists")

        self.Collection[Name] = LayoutItemInstance

    def GetLoadedObjectsAsList(self) -> list[LayoutItem]:
        return [self.Collection[key] for key in self.Collection]

    def GetLoadedObjectsAsDictionary(self) -> dict[str, LayoutItem]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> LayoutItem:
        return self.Collection[Name]
