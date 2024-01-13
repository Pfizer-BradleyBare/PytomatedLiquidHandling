from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.BaseClasses import UniqueObjectTrackerABC

from .AssignedWell import AssignedWell


@dataclass
class AssignedWellTracker(UniqueObjectTrackerABC[AssignedWell]):
    ...
