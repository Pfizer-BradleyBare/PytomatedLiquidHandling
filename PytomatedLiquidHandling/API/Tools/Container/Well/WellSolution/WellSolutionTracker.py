from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .WellSolution import WellSolution


@dataclass
class WellSolutionTracker(UniqueObjectTrackerABC[WellSolution]):
    ...
