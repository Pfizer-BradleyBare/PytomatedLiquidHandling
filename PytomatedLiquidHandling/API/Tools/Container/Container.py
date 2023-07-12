from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import (
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)

from .Well import Well


@dataclass
class Container(UniqueObjectABC, UniqueObjectTrackerABC[Well]):
    ...
