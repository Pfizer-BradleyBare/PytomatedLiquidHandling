from .....AbstractClasses import TrackerABC
from .Solution.WellSolutionTracker import WellSolutionTracker


class WellTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, WellSolutionTracker] = dict()

    def LoadManual(self, WellSolutionTrackerInstance: WellSolutionTracker):
        Name = WellSolutionTrackerInstance.GetWellNumber()

        if str(Name) in self.Collection:
            raise Exception("Well Already Exists")

        self.Collection[Name] = WellSolutionTrackerInstance

    def GetObjectsAsList(self) -> list[WellSolutionTracker]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, WellSolutionTracker]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> WellSolutionTracker:
        return self.Collection[Name]
