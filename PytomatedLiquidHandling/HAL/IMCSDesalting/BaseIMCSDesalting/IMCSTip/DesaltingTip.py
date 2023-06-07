from .....Tools.AbstractClasses import UniqueObjectABC, UniqueObjectTrackerABC
from dataclasses import dataclass
from .ElutionParameters import ElutionParameters
from enum import Enum


@dataclass
class DesaltingTip(UniqueObjectABC, UniqueObjectTrackerABC[ElutionParameters]):
    class TipTypes(Enum):
        SizeX100 = "SizeX100"
        SizeX150 = "SizeX150"
