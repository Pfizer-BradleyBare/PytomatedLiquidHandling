from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from . import LayoutItemABC


@dataclass
class LayoutItemTracker(UniqueObjectTrackerABC[LayoutItemABC]):
    pass
