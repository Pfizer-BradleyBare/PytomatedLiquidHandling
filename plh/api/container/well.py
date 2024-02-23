from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Callable, TypeVar, cast

from plh.hal import labware

from .liquid import Liquid, LiquidVolume
from .property import LiquidPropertyBase, PropertyWeight, PropertyWeightVolume

T = TypeVar("T", bound="LiquidPropertyBase")


@dataclass(init=False)
class Well:
    """A programmatic well that contains a liquid or mixture of liquids."""

    liquids: dict[Liquid, float] = field(
        init=False,
        default_factory=dict,
    )
    """Liquids and associated volume contained in the well."""

    def __init__(self: Well, *initial_liquids: LiquidVolume):
        self.liquids = {}

        for liquid_volume in initial_liquids:
            if liquid_volume.liquid in self.liquids:
                self.liquids[liquid_volume.liquid] += liquid_volume.volume
            else:
                self.liquids[liquid_volume.liquid] = liquid_volume.volume

    def __hash__(self: Well) -> int:
        return hash(id(self))

    def __eq__(self: Well, __value: object) -> bool:
        return self is __value

    def get_total_volume(self: Well) -> float:
        """Total volume present in the well."""
        return sum(self.liquids.values())

    def aspirate(self: Well, volume: float) -> list[LiquidVolume]:
        """Aspirate a volume from the well. Returns a list of (liquid,volume) that was aspirated."""
        aspirated_liquids: list[LiquidVolume] = []

        total_volume = self.get_total_volume()

        if volume > total_volume:
            msg = "You are removing more liquid than is available in the wells. This is weird."
            raise ValueError(msg)

        removed_fraction = volume / total_volume

        for liquid, volume in copy.copy(self.liquids).items():
            removed_volume = volume * removed_fraction
            new_volume = volume - removed_volume

            aspirated_liquids.append(LiquidVolume(liquid, removed_volume))

            if new_volume > 0:
                self.liquids[liquid] = new_volume
            else:
                del self.liquids[liquid]

        return aspirated_liquids

    def dispense(self: Well, liquid_volumes: list[LiquidVolume]) -> None:
        """Dispense a list of (liquid,volume) into a well."""
        for dispensed_liquid_volume in liquid_volumes:

            liquid = dispensed_liquid_volume.liquid

            current_volume = 0
            if liquid in self.liquids:
                current_volume = self.liquids[liquid]

            self.liquids[liquid] = dispensed_liquid_volume.volume + current_volume

    def get_well_property(
        self: Well,
        property_function: Callable[[Liquid], PropertyWeight[T]],
    ) -> T:
        """Get a specific liquid property based on the composition of liquids in the well."""
        if len(self.liquids) == 0:
            msg = "Well is empty."
            raise ValueError(msg)

        property_volumes = [
            PropertyWeightVolume(property_function(liquid), volume)
            for liquid, volume in self.liquids.items()
        ]

        return cast(
            T,
            cast(
                LiquidPropertyBase,
                property_volumes[0].property_weight.property,
            ).calculate_composition_property(
                property_volumes,
            ),
        )


@dataclass(init=False)
class SimulationWell(Well):
    """Combined a programmatic well with a physical labware to perform api simulations."""

    labware: labware.LabwareBase
    """labware that will be used for simultion of the api functions."""

    def __init__(
        self: SimulationWell,
        labware: labware.LabwareBase,
        *initial_liquids: LiquidVolume,
    ) -> None:
        Well.__init__(self, *initial_liquids)
        self.labware = labware
