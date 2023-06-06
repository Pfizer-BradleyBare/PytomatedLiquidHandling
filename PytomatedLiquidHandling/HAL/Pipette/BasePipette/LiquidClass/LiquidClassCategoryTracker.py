from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from .LiquidClassCategory import LiquidClassCategory
from dataclasses import dataclass


@dataclass
class LiquidClassCategoryTracker(UniqueObjectTrackerABC[LiquidClassCategory]):
    ...
