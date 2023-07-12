from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .DesaltingTip import DesaltingTip


@dataclass
class DesaltingTipTracker(UniqueObjectTrackerABC[DesaltingTip]):
    ...
