from .Solution.WellSolutionTracker import WellSolutionTracker
from .....AbstractClasses import ObjectABC


class Well(ObjectABC):
    def __init__(self, WellNumber: int):
        self.WellNumber: int = WellNumber
        self.WellSolutionTrackerInstance: WellSolutionTracker = WellSolutionTracker()

        self.MaxWellVolume: float = 0  # Can only be greater than 0
        self.MinWellVolume: float = 0  # can only be less than 0

    def GetName(self) -> int:
        return self.WellNumber

    def GetMaxVolume(self) -> float:
        return self.MaxWellVolume

    def GetMinVolume(self) -> float:
        return self.MinWellVolume

    def GetWellSolutionTracker(self) -> WellSolutionTracker:
        return self.WellSolutionTrackerInstance
