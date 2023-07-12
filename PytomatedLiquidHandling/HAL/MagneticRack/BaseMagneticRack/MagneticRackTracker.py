from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .MagneticRackABC import MagneticRackABC


@dataclass
class MagneticRackTracker(UniqueObjectTrackerABC[MagneticRackABC]):
    ...
