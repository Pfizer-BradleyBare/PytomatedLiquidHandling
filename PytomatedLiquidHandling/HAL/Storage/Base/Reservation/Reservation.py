from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class Reservation(UniqueObjectABC):
    LayoutItemInstance: LayoutItem.Base.LayoutItemABC
