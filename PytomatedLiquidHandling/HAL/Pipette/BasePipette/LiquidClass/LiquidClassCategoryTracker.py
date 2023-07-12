from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .LiquidClassCategory import LiquidClassCategory


@dataclass
class LiquidClassCategoryTracker(UniqueObjectTrackerABC[LiquidClassCategory]):
    ...
