from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import (
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)

from .LiquidClass import LiquidClass


@dataclass
class LiquidClassCategory(UniqueObjectTrackerABC[LiquidClass], UniqueObjectABC):
    ...
