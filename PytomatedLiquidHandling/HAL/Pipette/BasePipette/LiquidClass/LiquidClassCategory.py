from .....Tools.AbstractClasses import UniqueObjectABC, UniqueObjectTrackerABC
from .LiquidClass import LiquidClass
from dataclasses import dataclass


@dataclass
class LiquidClassCategory(UniqueObjectTrackerABC[LiquidClass], UniqueObjectABC):
    ...
