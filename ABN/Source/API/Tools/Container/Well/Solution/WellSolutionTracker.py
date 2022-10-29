from ......AbstractClasses import TrackerABC, ObjectABC
from .WellSolution import WellSolution


class WellSolutionTracker(TrackerABC[WellSolution], ObjectABC):
    def __init__(self, WellNumber: str):
        TrackerABC.__init__(self)
        self.WellNumber: str = WellNumber
        self.Collection: dict[str, WellSolution] = dict()

    def GetName(self) -> str:
        return self.WellNumber
