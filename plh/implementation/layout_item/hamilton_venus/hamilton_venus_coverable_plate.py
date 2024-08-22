from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from ..coverable_plate_base import CoverablePlateBase
from ..pydantic_validators import validate_instance
from .hamilton_venus_layout_item_base import HamiltonVenusLayoutItemBase
from .hamilton_venus_lid import HamiltonVenusLid


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusCoverablePlate(HamiltonVenusLayoutItemBase, CoverablePlateBase):

    lid: Annotated[
        HamiltonVenusLid,
        BeforeValidator(validate_instance),
    ]
