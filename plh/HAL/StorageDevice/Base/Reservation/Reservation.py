from dataclasses import field

from pydantic import dataclasses

from PytomatedLiquidHandling.HAL import LayoutItem


@dataclasses.dataclass(kw_only=True)
class Reservation:
    LayoutItem: LayoutItem.Base.LayoutItemABC
    _IsStored: bool = field(init=False, default=False)
