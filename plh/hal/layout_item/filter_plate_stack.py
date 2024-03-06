from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from .coverable_filter_plate import CoverableFilterPlate
from .coverable_plate import CoverablePlate
from .filter_plate import FilterPlate
from .layout_item_base import *
from .plate import Plate
from .pydantic_validators import validate_instance


@dataclasses.dataclass(kw_only=True, eq=False)
class FilterPlateStack:
    """A filter plate stack is made of two parts: a filter plate, and a lower base labware to hold the filter plate.
    Filter plates generally have open bottom wells so the lower labware prevents contamination from contact with the carriers or deck.
    """

    filter_plate: Annotated[
        CoverableFilterPlate | FilterPlate,
        BeforeValidator(validate_instance),
    ]
    """The filter plate."""

    base: Annotated[
        Plate | CoverablePlate,
        BeforeValidator(validate_instance),
    ]
    """The layout item upon which the filter plate is placed."""
