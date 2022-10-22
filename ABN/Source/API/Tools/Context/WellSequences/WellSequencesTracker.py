from ....AbstractClasses import TrackerABC
from .WellSequences import WellSequences


class WellSequencesTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[int, WellSequences] = dict()

    def LoadManual(self, WellSequencesTrackerInstance: WellSequences):
        Name = WellSequencesTrackerInstance.GetName()

        if Name in self.Collection:
            raise Exception("Well Already Exists")

        self.Collection[Name] = WellSequencesTrackerInstance

    def GetObjectsAsList(self) -> list[WellSequences]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[int, WellSequences]:
        return self.Collection

    def GetObjectByName(self, Name: int) -> WellSequences:
        return self.Collection[Name]
