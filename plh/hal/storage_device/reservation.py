from dataclasses import field

from pydantic import dataclasses

from plh.hal import layout_item


@dataclasses.dataclass(kw_only=True)
class Reservation:
    """Information about a reservated position."""

    layout_item: layout_item.LayoutItemBase
    """The position reserved."""

    is_stored: bool = field(init=False, default=False)
    """Is an object current in this position."""
