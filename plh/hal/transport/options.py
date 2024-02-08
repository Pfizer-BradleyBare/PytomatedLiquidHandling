from __future__ import annotations

from pydantic import dataclasses

from plh.hal import layout_item


@dataclasses.dataclass(kw_only=True)
class GetPlaceOptions:
    """Options passed to transport"""

    source_layout_item: layout_item.LayoutItemBase
    """Layout item to get."""

    destination_layout_item: layout_item.LayoutItemBase
    """Layout item where you will placed the getted layout item."""
