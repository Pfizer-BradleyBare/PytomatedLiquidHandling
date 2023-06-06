from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .Options import Options
from dataclasses import dataclass


@dataclass
class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    ...
