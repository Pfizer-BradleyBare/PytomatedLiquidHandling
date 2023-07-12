from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .IMCSDesaltingABC import IMCSDesaltingABC


@dataclass
class IMCSDesaltingTracker(UniqueObjectTrackerABC[IMCSDesaltingABC]):
    ...
