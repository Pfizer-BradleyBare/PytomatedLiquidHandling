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

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: LayoutItem) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: LayoutItem) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[LayoutItem]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, LayoutItem]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> LayoutItem:
        return self.Collection[Name]
