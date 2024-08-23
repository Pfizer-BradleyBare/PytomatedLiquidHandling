from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from ..filter_plate_base import FilterPlateBase
from ..pydantic_validators import validate_instance
from .hamilton_venus_coverable_plate import HamiltonVenusCoverablePlate
from .hamilton_venus_layout_item_base import HamiltonVenusLayoutItemBase
from .hamilton_venus_plate import HamiltonVenusPlate


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusFilterPlate(HamiltonVenusLayoutItemBase, FilterPlateBase):
    """A plate that contains a filter. Filter plates  are always placed atop a collection plate. Useful for vacuum and centrifuge filtrations."""

    collection_plate: Annotated[
        HamiltonVenusPlate | HamiltonVenusCoverablePlate,
        BeforeValidator(validate_instance),
    ]
    """The layout item upon which the filter plate is placed."""
