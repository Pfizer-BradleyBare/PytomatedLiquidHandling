from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses, field_validator
from pydantic.functional_validators import BeforeValidator

from plh.hal import tip

from .liquid_class import LiquidClass


@dataclasses.dataclass(kw_only=True)
class PipetteTip:
    tip: Annotated[tip.TipBase, BeforeValidator(tip.validate_instance)]
    tip_support_dropoff_labware_id: str
    tip_support_pickup_labware_id: str
    tip_waste_labware_id: str
    supported_aspirate_liquid_class_categories: dict[str, list[LiquidClass]]
    supported_dispense_liquid_class_categories: dict[str, list[LiquidClass]]

    @field_validator("supported_liquid_class_categories", mode="after")
    @classmethod
    def __supported_liquid_class_categories_valdate(
        cls: type[PipetteTip],
        v: dict,
    ) -> dict:
        for category in v:
            v[category] = sorted(v[category], key=lambda x: x.max_volume)

        return v

    def is_liquid_class_category_supported(self: PipetteTip, category: str) -> bool:
        return category in self.supported_aspirate_liquid_class_categories
