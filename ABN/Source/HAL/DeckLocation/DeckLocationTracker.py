from ...AbstractClasses import TrackerABC
from .DeckLocation import DeckLocation
from ..Transport import TransportTracker


class DeckLocationTracker(TrackerABC):
    def __init__(self, TransportTrackerInstance: TransportTracker):
        self.Collection: dict[str, DeckLocation] = dict()
        self.TransportTrackerInstance: TransportTracker = TransportTrackerInstance

    def ManualLoad(self, ObjectABCInstance: DeckLocation) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is already tracked"
            )

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: DeckLocation) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is not yet tracked"
            )

        del self.Collection[ObjectABCInstance.GetName()]

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
