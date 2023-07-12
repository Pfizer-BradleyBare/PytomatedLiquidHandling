from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .CarrierABC import CarrierABC


@dataclass
class CarrierTracker(UniqueObjectTrackerABC[CarrierABC]):
    pass
