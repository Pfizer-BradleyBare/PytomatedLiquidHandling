from ......AbstractClasses import TrackerABC, ObjectABC
from .WellSolution import WellSolution


class WellSolutionTracker(TrackerABC[WellSolution], ObjectABC):
    def __init__(self, WellNumber: int):
        TrackerABC.__init__(self)
        self.WellNumber: int = WellNumber
        self.Collection: dict[str, WellSolution] = dict()

    def GetName(self) -> int:
        return self.WellNumber
