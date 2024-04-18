from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Callable, TypeVar, cast

from .liquid import Liquid
from .property import LiquidPropertyBase

T = TypeVar("T", bound="LiquidPropertyBase")


@dataclass(init=False)
class Well:
    """A programmatic well that contains a liquid or mixture of liquids."""

    liquids: dict[Liquid, float] = field(
        init=False,
        default_factory=dict,
    )
    """Liquids and associated volume contained in the well."""

    def __init__(self: Well, *initial_liquids: tuple[Liquid, float]):
        self.liquids = {}

        for liquid, volume in initial_liquids:
            if liquid in self.liquids:
                self.liquids[liquid] += volume
            else:
                self.liquids[liquid] = volume

    def __hash__(self: Well) -> int:
        return hash(id(self))

    def __eq__(self: Well, __value: object) -> bool:
        return self is __value

    def get_total_volume(self: Well) -> float:
        """Total volume present in the well."""
        return sum(self.liquids.values())

    def aspirate(self: Well, volume: float) -> list[tuple[Liquid, float]]:
        """Aspirate a volume from the well. Returns a list of (liquid,volume) that was aspirated."""
        aspirated_liquids: list[tuple[Liquid, float]] = []

        total_volume = self.get_total_volume()

        if volume > total_volume:
            msg = "You are removing more liquid than is available in the wells. This is weird."
            raise ValueError(msg)

        removed_fraction = volume / total_volume

        for liquid, volume in copy.copy(self.liquids).items():
            removed_volume = volume * removed_fraction
            new_volume = volume - removed_volume

            aspirated_liquids.append((liquid, removed_volume))

            if new_volume > 0:
                self.liquids[liquid] = new_volume
            else:
                del self.liquids[liquid]

        return aspirated_liquids

    def dispense(self: Well, liquid_volumes: list[tuple[Liquid, float]]) -> None:
        """Dispense a list of (liquid,volume) into a well."""
        for liquid, volume in liquid_volumes:

            current_volume = 0
            if liquid in self.liquids:
                current_volume = self.liquids[liquid]

            self.liquids[liquid] = volume + current_volume

    def get_well_property(
        self: Well,
        property_function: Callable[[Liquid], tuple[T, int]],
    ) -> T:
        """Get a specific liquid property based on the composition of liquids in the well."""
        if len(self.liquids) == 0:
            msg = "Well is empty."
            raise ValueError(msg)

        property_volumes = [
            (property_function(liquid), volume)
            for liquid, volume in self.liquids.items()
        ]

        return cast(
            T,
            cast(
                LiquidPropertyBase,
                property_volumes[0][0][0],
            ).calculate_composition_property(
                property_volumes,
            ),
        )
