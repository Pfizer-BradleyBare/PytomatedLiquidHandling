from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .AssignedWell import AssignedWell


@dataclass
class AssignedWellTracker(UniqueObjectTrackerABC[AssignedWell]):
    ...
