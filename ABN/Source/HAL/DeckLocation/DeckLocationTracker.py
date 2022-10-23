from ...AbstractClasses import TrackerABC
from .DeckLocation import DeckLocation
from ..Transport import TransportTracker


class DeckLocationTracker(TrackerABC):
    def __init__(self, TransportTrackerInstance: TransportTracker):
        self.Collection: dict[str, DeckLocation] = dict()
        self.TransportTrackerInstance: TransportTracker = TransportTrackerInstance

    def ManualLoad(self, ObjectABCInstance: DeckLocation) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: DeckLocation) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: DeckLocation) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[DeckLocation]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, DeckLocation]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> DeckLocation:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
