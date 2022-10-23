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

    def ManualLoad(self, ObjectABCInstance: LayoutItem) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: LayoutItem) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: LayoutItem) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[LayoutItem]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, LayoutItem]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> LayoutItem:
        return self.Collection[Name]
