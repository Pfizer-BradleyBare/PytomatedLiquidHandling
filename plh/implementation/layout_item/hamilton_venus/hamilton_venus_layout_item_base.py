from __future__ import annotations

from pydantic import dataclasses

from ..layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusLayoutItemBase(LayoutItemBase):

    labware_id: str
    """Labware id from the automation software for this deck position."""
