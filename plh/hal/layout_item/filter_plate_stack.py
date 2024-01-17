from __future__ import annotations

from pydantic import dataclasses

from plh.hal import labware

from .coverable_filter_plate import CoverableFilterPlate
from .filter_plate import FilterPlate
from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True)
class FilterPlateStack(LayoutItemBase):
    labware: labware.NonPipettableLabware
    filter_plate: CoverableFilterPlate | FilterPlate
