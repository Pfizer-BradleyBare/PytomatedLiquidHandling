from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.BaseClasses import UniqueObjectTrackerABC

from .DesaltingTip import DesaltingTip


@dataclass
class DesaltingTipTracker(UniqueObjectTrackerABC[DesaltingTip]):
    ...
