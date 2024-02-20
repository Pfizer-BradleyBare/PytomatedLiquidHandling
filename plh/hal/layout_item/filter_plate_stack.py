from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import labware

from .coverable_filter_plate import CoverableFilterPlate
from .filter_plate import FilterPlate
from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class FilterPlateStack(LayoutItemBase):
    """TODO"""

    labware: Annotated[
        labware.NonPipettableLabware,
        BeforeValidator(labware.validate_instance),
    ]
    filter_plate: CoverableFilterPlate | FilterPlate
