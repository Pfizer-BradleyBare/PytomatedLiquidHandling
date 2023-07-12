from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .Tip import Tip


@dataclass
class TipTracker(UniqueObjectTrackerABC[Tip]):
    ...
