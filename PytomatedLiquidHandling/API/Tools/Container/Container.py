from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import (
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)
from PytomatedLiquidHandling.HAL import Labware
from .Well import Well


@dataclass
class Container(UniqueObjectABC, UniqueObjectTrackerABC[Well]):
    LabwareInstance: Labware.PipettableLabware
