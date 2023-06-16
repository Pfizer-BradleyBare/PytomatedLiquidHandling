from dataclasses import dataclass

from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .CarrierABC import CarrierABC


@dataclass
class CarrierTracker(UniqueObjectTrackerABC[CarrierABC]):
    pass
