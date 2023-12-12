from PytomatedLiquidHandling.HAL import LayoutItem
from pydantic import dataclasses
from dataclasses import field


@dataclasses.dataclass(kw_only=True)
class Reservation:
    LayoutItem: LayoutItem.Base.LayoutItemABC
    _IsStored: bool = field(init=False, default=False)
