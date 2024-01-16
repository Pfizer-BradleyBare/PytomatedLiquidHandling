from dataclasses import field

from pydantic import dataclasses

from plh.hal import layout_item


@dataclasses.dataclass(kw_only=True)
class Reservation:
    layout_item: layout_item.LayoutItemBase
    is_stored: bool = field(init=False, default=False)
