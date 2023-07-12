from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from . import LabwareABC


@dataclass
class LabwareTracker(UniqueObjectTrackerABC[LabwareABC]):
    pass
