from dataclasses import field

from pydantic import dataclasses

from plh.hal import LayoutItem


@dataclasses.dataclass(kw_only=True)
class Reservation:
    LayoutItem: LayoutItem.Base.LayoutItemBase
    _IsStored: bool = field(init=False, default=False)
