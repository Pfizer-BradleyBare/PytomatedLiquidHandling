from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from . import ClosedContainerABC


@dataclass
class ClosedContainerTracker(UniqueObjectTrackerABC[ClosedContainerABC]):
    pass
