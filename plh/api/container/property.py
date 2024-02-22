from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, TypeVar

T = TypeVar("T", bound="LiquidPropertyBase")


class LiquidPropertyBase(Enum):
    """Base enum for defining liquid properties. All items should be auto()."""

    @classmethod
    def calculate_composition_property(
        cls: type[LiquidPropertyBase],
        property_volumes: list[PropertyWeightVolume],
    ) -> LiquidPropertyBase:
        """Will calculate the combined property for a composition given a list of volumes and property values."""
        if len(property_volumes) == 0:
            raise ValueError("List must contain at least 1 item.")

        if not all(
            isinstance(item.property_weight.property, cls) for item in property_volumes
        ):
            msg = "All property values must be from the same property."
            raise ValueError(msg)

        total_volume = sum(
            property_volume.volume for property_volume in property_volumes
        )

        property_contributions = []

        for property_volume in property_volumes:
            part_per_hundred = int(property_volume.volume * 100 / total_volume)
            # Each property is a percentage of the solution. We convert to part_per_hundred to make the math easier.

            property_contributions += (
                [property_volume.property_weight.property.value]
                * part_per_hundred
                * property_volume.property_weight.weight
            )
            # We add the property numeric value to a list part_per_hundred * weight times.
            # If we do this for all properties then we can get the average property for the composition.

        return cls(
            round(sum(property_contributions) / len(property_contributions)),
        )
        # Because each numeric value is unique and they are grouped by each property we can round the
        # average property value to get the most similar property that describes the composition.


class Volatility(LiquidPropertyBase):
    """Solution property that represents Voltatility."""

    LOW = auto()
    """Similar to glycerol."""

    MEDIUM = auto()
    """Similar to water."""

    HIGH = auto()
    """Similar to MeOH."""


class Viscosity(LiquidPropertyBase):
    """Solution property that represents Viscosity."""

    LOW = auto()
    """Similar to MeOH."""

    MEDIUM = auto()
    """Similar to water."""

    HIGH = auto()
    """Similar to glycerol."""


class Homogeneity(LiquidPropertyBase):
    """Solution property that represents Homogeneity."""

    HOMOGENOUS = auto()
    """Similar to salt dissolved in a liquid."""

    EMULSION = auto()
    """Similar to oil mixed with water using a surfactant."""

    SUSPENSION = auto()
    """Similar to colloidal suspension."""

    HETERGENOUS = auto()
    """Similar to colloidal suspension BUT the particulate does not stay suspended without mixing."""


class Polarity(LiquidPropertyBase):
    """Solution property that represents Polarity."""

    NON_POLAR = auto()
    """Similar to chloroform. Low to no conductivity."""

    POLAR = auto()
    """Similar to water. Medium to high conductivity."""


@dataclass(frozen=True)
class PropertyWeight(Generic[T]):
    """Grouping of a weight value for a liquid property."""

    property: T
    """Any property that inherits ```LiquidPropertyBase```."""

    weight: int = 1
    """The weight of this part in a solution composition."""


@dataclass(frozen=True)
class PropertyWeightVolume:
    """A volume of a given weighted property."""

    property_weight: PropertyWeight
    """The weighted property."""

    volume: float
    """The volume of the weighted property."""
