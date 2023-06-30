from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import LayoutItem

from .....Tools.AbstractClasses import UniqueObjectABC


@dataclass
class Reservation(UniqueObjectABC):
    LayoutItemInstance: LayoutItem.BaseLayoutItem.LayoutItemABC
