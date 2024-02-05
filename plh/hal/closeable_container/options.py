from __future__ import annotations

from pydantic import dataclasses

from plh.hal import layout_item


@dataclasses.dataclass(kw_only=True)
class OpenCloseOptions:
    """Options that can be used for ```open```, ```open_time```, ```close```, or ```close_time```."""

    layout_item: layout_item.LayoutItemBase
    """Compatible layout item you want to open/close."""

    position: str | int
    """Position to open/close. NOTE: position will be converted to correct type (alpha vs numeric) based on labware layout info.
    NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    """
