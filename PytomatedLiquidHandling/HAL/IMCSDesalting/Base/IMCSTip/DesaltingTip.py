from dataclasses import dataclass
from enum import Enum

from PytomatedLiquidHandling.Tools.BaseClasses import (
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)

from .ElutionParameters import ElutionParameters


@dataclass
class DesaltingTip(UniqueObjectABC, UniqueObjectTrackerABC[ElutionParameters]):
    class TipTypes(Enum):
        SizeX100 = "SizeX100"
        SizeX150 = "SizeX150"
