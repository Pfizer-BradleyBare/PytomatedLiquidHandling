from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import tip

from .liquid_class import LiquidClass


@dataclasses.dataclass(kw_only=True)
class PipetteTip:
    tip: Annotated[tip.TipBase, BeforeValidator(tip.validate_instance)]
    tip_support_dropoff_labware_id: str
    tip_support_pickup_labware_id: str
    supported_aspirate_liquid_class_categories: dict[str, list[LiquidClass]]
    supported_dispense_liquid_class_categories: dict[str, list[LiquidClass]]
