from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .PipetteTip import PipetteTip


@dataclass
class PipetteTipTracker(UniqueObjectTrackerABC[PipetteTip]):
    ...
