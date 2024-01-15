from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import dataclasses

from .layout_item_base import LayoutItemBase

if TYPE_CHECKING:
    from plh.hal import labware

    from .coverable_filter_plate import CoverableFilterPlate
    from .filter_plate import FilterPlate


@dataclasses.dataclass(kw_only=True)
class FilterPlateStack(LayoutItemBase):
    labware: labware.NonPipettableLabware
    filter_plate: CoverableFilterPlate | FilterPlate
