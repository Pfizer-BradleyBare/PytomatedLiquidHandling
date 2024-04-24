from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import tip

from .liquid_class import LiquidClass


@dataclasses.dataclass(kw_only=True)
class PipetteTip:
    tip: Annotated[tip.TipBase, BeforeValidator(tip.validate_instance)]
    tip_support_dropoff_labware_id: str
    tip_support_pickup_labware_id: str
    supported_aspirate_liquid_class_categories: dict[str, list[LiquidClass]]
    supported_dispense_liquid_class_categories: dict[str, list[LiquidClass]]

    def __post_init__(self: PipetteTip) -> None:
        self.supported_aspirate_liquid_class_categories = {
            category: sorted(liquid_classes, key=lambda x: x.max_volume)
            for category, liquid_classes in self.supported_aspirate_liquid_class_categories.items()
        }
        self.supported_dispense_liquid_class_categories = {
            category: sorted(liquid_classes, key=lambda x: x.max_volume)
            for category, liquid_classes in self.supported_dispense_liquid_class_categories.items()
        }

    def __hash__(self: PipetteTip) -> int:
        return self.tip.__hash__()

    def __eq__(self: PipetteTip, __value: PipetteTip) -> bool:
        return self.tip.__eq__(__value.tip)

    @staticmethod
    def _get_liquid_class(
        liquid_class_categories: dict[str, list[LiquidClass]],
        category: str,
        volume: float,
    ) -> LiquidClass:
        if category not in liquid_class_categories:
            raise ValueError("Category not available for this pipette tip.")

        for liquid_class in liquid_class_categories[category]:
            if liquid_class.min_volume <= volume <= liquid_class.max_volume:
                return liquid_class

        raise ValueError(
            "Category and volume combination not supported by this pipette tip.",
        )

    def get_aspirate_liquid_class(
        self: PipetteTip,
        category: str,
        volume: float,
    ) -> LiquidClass:
        return self._get_liquid_class(
            self.supported_aspirate_liquid_class_categories,
            category,
            volume,
        )

    def get_dispense_liquid_class(
        self: PipetteTip,
        category: str,
        volume: float,
    ) -> LiquidClass:
        return self._get_liquid_class(
            self.supported_dispense_liquid_class_categories,
            category,
            volume,
        )
