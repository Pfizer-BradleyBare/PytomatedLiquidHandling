from __future__ import annotations

from pydantic import dataclasses, field_validator

from plh.hal import tip

from .liquid_class import LiquidClass


@dataclasses.dataclass(kw_only=True)
class PipetteTip:
    tip: tip.TipBase
    tip_support_dropoff_labware_id: str
    tip_support_pickup_labware_id: str
    tip_waste_labware_id: str
    supported_liquid_class_categories: dict[str, list[LiquidClass]]

    @field_validator("tip", mode="before")
    @classmethod
    def __tip_validate(cls: type[PipetteTip], v: str | tip.TipBase) -> tip.TipBase:
        if isinstance(v, tip.TipBase):
            return v

        objects = tip.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier + " is not found in " + tip.TipBase.__name__ + " objects.",
            )

        return objects[identifier]

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
        return category in self.supported_liquid_class_categories
