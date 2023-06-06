from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....LayoutItem import CoverablePosition, NonCoverablePosition
from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(NonUniqueObjectABC):
    LayoutItemInstance: CoverablePosition | NonCoverablePosition
    Position: int
