from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Callable, ClassVar

__all__ = [
    "Container",
    "Well",
    "Liquid",
    "LiquidPropertyBase",
    "LiquidPropertyValue",
    "Volatility",
    "Viscosity",
    "Homogeneity",
    "Polarity",
]


@dataclass
class LiquidPropertyValue:
    """Representative value for a ```LiquidPropertyBase```.
    Values are a high level representation of "Low", "Medium", "High", etc.
    """

    _numeric_value_counter: ClassVar[int] = 1
    """A unique value for each new ```LiquidPropertyValue```. Autoincremented after assignment to ensure uniqueness."""

    numeric_value: int = field(init=False)
    """Value used for composition calculations. Must be unique. Autoassigned."""

    def __post_init__(self):
        self.numeric_value = LiquidPropertyValue._numeric_value_counter
        LiquidPropertyValue._numeric_value_counter += 1


class LiquidPropertyBase(Enum):
    """Base enum for defining liquid properties."""

    @classmethod
    def __init_subclass__(cls: type[LiquidPropertyBase]) -> None:
        """Ensure that all ```LiquidPropertyBase``` items are of type ```LiquidPropertyValue```."""
        for item in cls:
            if not isinstance(item.value, LiquidPropertyValue):
                msg = f"{item} is not of type LiquidPropertyValue."
                raise TypeError(msg)

    @classmethod
    def _get_by_numeric_value(
        cls: type[LiquidPropertyBase],
        value: int,
    ) -> LiquidPropertyBase:
        for item in cls:
            if item.value.numeric_value == value:
                return item

        msg = f"No numeric key match found for {value}."
        raise ValueError(msg)

    @classmethod
    def calculate_composition_property(
        cls: type[LiquidPropertyBase],
        property_volumes: list[tuple[tuple[LiquidPropertyBase, int], float]],
    ) -> LiquidPropertyBase:
        """Will calculate the combined property for a composition given a list of volumes and property values."""
        if len(property_volumes) == 0:
            raise ValueError("List must contain at least 1 item.")

        if not all(isinstance(item[0][0], cls) for item in property_volumes):
            msg = "All property values must be from the same property."
            raise ValueError(msg)

        total_volume = sum(property_volume[1] for property_volume in property_volumes)

        property_contributions = []

        for property_volume in property_volumes:
            part_per_hundred = int(property_volume[1] * 100 / total_volume)
            # Each property is a percentage of the solution. We convert to part_per_hundred to make the math easier.

            property_contributions += (
                [property_volume[0][0].value.numeric_value]
                * part_per_hundred
                * property_volume[0][1]
            )
            # We add the property numeric value to a list part_per_hundred * weight times.
            # If we do this for all properties then we can get the average property for the composition.

        return cls._get_by_numeric_value(
            round(sum(property_contributions) / len(property_contributions)),
        )
        # Because each numeric value is unique and they are grouped by each property we can round the
        # average property value to get the most similar property that describes the composition.


class Volatility(LiquidPropertyBase):
    """Solution property that represents Voltatility."""

    LOW = LiquidPropertyValue()
    """Similar to glycerol."""

    MEDIUM = LiquidPropertyValue()
    """Similar to water."""

    HIGH = LiquidPropertyValue()
    """Similar to MeOH."""


class Viscosity(LiquidPropertyBase):
    """Solution property that represents Viscosity."""

    LOW = LiquidPropertyValue()
    """Similar to MeOH."""

    MEDIUM = LiquidPropertyValue()
    """Similar to water."""

    HIGH = LiquidPropertyValue()
    """Similar to glycerol."""


class Homogeneity(LiquidPropertyBase):
    """Solution property that represents Homogeneity."""

    HOMOGENOUS = LiquidPropertyValue()
    """Similar to salt dissolved in a liquid."""

    EMULSION = LiquidPropertyValue()
    """Similar to oil mixed with water using a surfactant."""

    SUSPENSION = LiquidPropertyValue()
    """Similar to colloidal suspension."""

    HETERGENOUS = LiquidPropertyValue()
    """Similar to colloidal suspension BUT the particulate does not stay suspended without mixing."""


class Polarity(LiquidPropertyBase):
    """Solution property that represents Polarity."""

    NON_POLAR = LiquidPropertyValue()
    """Similar to chloroform. Low to no conductivity."""

    POLAR = LiquidPropertyValue()
    """Similar to water. Medium to high conductivity."""


@dataclass
class Liquid:
    """A representation of a liquid in a physical well.
    A liquid will be described by a name and physical properties. For now a liquid is defined as having 4 properties:
    ```Volatility```, ```Viscosity```, ```Homogeneity```,and ```Polarity```.
    """

    name: str
    """The liquid name."""

    volatility_property: tuple[Volatility, int]
    """The voltaility property and weight for the liquid.
    For example: ACN mixed with water still makes a solution significantly non-viscous but only slightly volatile."""

    viscosity_property: tuple[Viscosity, int]
    """The viscosity property and weight for the liquid.
    For example: ACN mixed with water still makes a solution significantly non-viscous but only slightly volatile."""

    homogeneity_property: tuple[Homogeneity, int]
    """The homogeneity property and weight for the liquid.
    For example: It's possible to have a reagent that causes a precipitation.
    A small amount of reagent added would have to have a huge weight to change the composition."""

    polarity_property: tuple[Polarity, int]
    """The polarity property and weight for the liquid.
    For example: Chloroform is not conductive at all. But a small amount of water will add significant polarity."""


@dataclass
class Well:
    """A physical well that contains a liquid or mixture of liquids."""

    liquid_volumes: dict[str, tuple[Liquid, float]] = field(
        init=False,
        default_factory=dict,
    )
    """Liquids and associated volume contained in the well."""

    def get_total_volume(self: Well) -> float:
        """Total volume present in the well."""
        return sum(
            [liquid_volume[1] for liquid_volume in self.liquid_volumes.values()],
        )

    def aspirate(self: Well, volume: float) -> list[tuple[Liquid, float]]:
        """Aspirate a volume from the well. Returns a list of (liquid,volume) that was aspirated."""
        aspirated_liquids: list[tuple[Liquid, float]] = []

        total_volume = self.get_total_volume()

        if volume > total_volume:
            msg = "You are removing more liquid than is available in the wells. This is weird."
            raise ValueError(msg)

        removed_fraction = volume / total_volume

        for key, liquid_volume in self.liquid_volumes.items():
            removed_volume = liquid_volume[1] * removed_fraction
            new_volume = liquid_volume[1] - removed_volume

            aspirated_liquids.append((liquid_volume[0], removed_volume))

            if new_volume > 0:
                self.liquid_volumes[key] = (liquid_volume[0], new_volume)
            else:
                del self.liquid_volumes[key]

        return aspirated_liquids

    def dispense(self: Well, liquid_volumes: list[tuple[Liquid, float]]) -> None:
        """Dispense a list of (liquid,volume) into a well."""
        for dispensed_liquid_volume in liquid_volumes:

            name = dispensed_liquid_volume[0].name

            current_volume = 0
            if name in self.liquid_volumes:
                current_volume = self.liquid_volumes[name][1]

            self.liquid_volumes[name] = (
                dispensed_liquid_volume[0],
                dispensed_liquid_volume[1] + current_volume,
            )

    def get_well_property(
        self: Well,
        property_function: Callable[[Liquid], tuple[LiquidPropertyBase, int]],
    ) -> LiquidPropertyBase:
        """Get a specific liquid property based on the composition of liquids in the well."""
        if len(self.liquid_volumes) == 0:
            msg = "Well is empty."
            raise ValueError(msg)

        property_volumes = [
            (property_function(liquid_volume[0]), liquid_volume[1])
            for liquid_volume in self.liquid_volumes.values()
        ]

        return property_volumes[0][0][0].calculate_composition_property(
            property_volumes,
        )


@dataclass
class Container:
    """A container with many wells. This is a programmatic representation of a physical object. The wells can span many different labware."""

    name: str
    """Name of the container."""

    wells: list[Well] = field(init=False, default_factory=list)
    """Separate wells used by the container."""

    num_wells: InitVar[int]
    """Number of wells this container will have. Initialization variable."""

    def __post_init__(self: Container, num_wells: int) -> None:
        for _ in range(num_wells):
            self.wells.append(Well())
