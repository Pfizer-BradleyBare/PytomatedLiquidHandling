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

    def ManualLoad(self, ObjectABCInstance: Lid) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Lid) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: Lid) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Lid]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, Lid]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Lid:
        return self.Collection[Name]
