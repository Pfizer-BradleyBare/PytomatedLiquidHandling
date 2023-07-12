from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .WellSolution.WellSolutionTracker import WellSolutionTracker


class Well(UniqueObjectABC):
    def __init__(self, WellNumber: int):
        UniqueObjectABC.__init__(self, WellNumber)
        self.WellSolutionTrackerInstance: WellSolutionTracker = WellSolutionTracker()

        self.MaxWellVolume: float = 0  # Can only be greater than 0
        self.MinWellVolume: float = 0  # can only be less than 0

    def GetWellSolutionTracker(self) -> WellSolutionTracker:
        return self.WellSolutionTrackerInstance
