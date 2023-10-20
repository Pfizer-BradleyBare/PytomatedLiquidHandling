from pydantic import BaseModel, PrivateAttr
from PytomatedLiquidHandling.HAL import LayoutItem


class Reservation(BaseModel):
    LayoutItem: LayoutItem.Base.LayoutItemABC
    _IsStored: bool = PrivateAttr(default=False)
