from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .StepABC import StepABC


@dataclass
class StepTracker(UniqueObjectTrackerABC[StepABC]):
    ...
