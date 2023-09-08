from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import LayoutItem


@dataclass
class Reservation:
    LayoutItem: LayoutItem.Base.LayoutItemABC
    IsStored: bool = field(init=False, default=False)
