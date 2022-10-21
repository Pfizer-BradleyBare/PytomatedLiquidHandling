from ......AbstractClasses import TrackerABC
from .WellSolution import WellSolution


class WellSolutionTracker(TrackerABC):
    def __init__(self, WellNumber: int):
        self.WellNumber: int = WellNumber
        self.Collection: dict[str, WellSolution] = dict()

    def GetWellNumber(self) -> int:
        return self.WellNumber

    def LoadManual(self, WellSolutionInstance: WellSolution):
        Name = WellSolutionInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Solution Already Exists")

        self.Collection[Name] = WellSolutionInstance
