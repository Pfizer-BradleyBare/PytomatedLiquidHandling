from ...AbstractClasses import TrackerABC
from .DeckLocation import DeckLocation
from ..Transport import TransportTracker


class DeckLocationTracker(TrackerABC):
    def __init__(self, TransportTrackerInstance: TransportTracker):
        self.Collection: dict[str, DeckLocation] = dict()
        self.TransportTrackerInstance: TransportTracker = TransportTrackerInstance

    def LoadManual(self, DeckLocationInstace: DeckLocation):
        Name = DeckLocationInstace.GetName()

        if Name in self.Collection:
            raise Exception("Deck Location Already Exists")

        self.Collection[Name] = DeckLocationInstace

    def GetLoadedObjectsAsDictionary(self) -> dict[str, DeckLocation]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[DeckLocation]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> DeckLocation:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
