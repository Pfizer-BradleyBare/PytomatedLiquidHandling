from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .MethodABC import MethodABC


@dataclass
class MethodTracker(UniqueObjectTrackerABC[MethodABC]):
    ...
