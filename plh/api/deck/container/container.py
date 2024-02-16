from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, ClassVar, Generic, TypeVar, cast

T = TypeVar("T",bound="LiquidPropertyBase")

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

        if not all(isinstance(item.property_weight.property, cls) for item in property_volumes):
            msg = "All property values must be from the same property."
            raise ValueError(msg)

        total_volume = sum(property_volume.volume for property_volume in property_volumes)

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
class LiquidVolume:
    """A volume of a given liquid."""

    liquid: Liquid
    """The ```Liquid```."""

    volume: float
    """The volume of the ```Liquid```."""

@dataclass(frozen=True)
class PropertyWeightVolume:
    """A volume of a given weighted property."""

    property_weight: PropertyWeight
    """The weighted property."""

    volume: float
    """The volume of the weighted property."""

@dataclass(frozen=True)
class Liquid:
    """A representation of a liquid in a physical well.
    A liquid will be described by a name and physical properties. For now a liquid is defined as having 4 properties:
    ```Volatility```, ```Viscosity```, ```Homogeneity```,and ```Polarity```.
    """

    name: str
    """The liquid name."""

    volatility_property: PropertyWeight[Volatility] = field(default=PropertyWeight(Volatility.MEDIUM))
    """The voltaility property and weight for the liquid.
    For example: ACN mixed with water still makes a solution significantly non-viscous but only slightly volatile."""

    viscosity_property: PropertyWeight[Viscosity] = field(default=PropertyWeight(Viscosity.MEDIUM))
    """The viscosity property and weight for the liquid.
    For example: ACN mixed with water still makes a solution significantly non-viscous but only slightly volatile."""

    homogeneity_property: PropertyWeight[Homogeneity] = field(default=PropertyWeight(Homogeneity.HOMOGENOUS))
    """The homogeneity property and weight for the liquid.
    For example: It's possible to have a reagent that causes a precipitation.
    A small amount of reagent added would have to have a huge weight to change the composition."""

    polarity_property: PropertyWeight[Polarity] = field(default=PropertyWeight(Polarity.POLAR))
    """The polarity property and weight for the liquid.
    For example: Chloroform is not conductive at all. But a small amount of water will add significant polarity."""


@dataclass
class Well:
    """A physical well that contains a liquid or mixture of liquids."""

    liquid_volumes: dict[str, LiquidVolume] = field(
        init=False,
        default_factory=dict,
    )
    """Liquids and associated volume contained in the well."""

    _hashable_counter: ClassVar[int] = 0
    _hashable_value: int = field(init=False)
    """Simple way to define a custom hashable value for this class to make it a dict key."""

    def __post_init__(self: Well) -> None:
        self._hashable_value = Well._hashable_counter
        Well._hashable_counter += 1

    def __hash__(self: Well) -> int:
        return hash(self._hashable_value)

    def __eq__(self:Well, __value: Well) -> bool:
        return self._hashable_value == __value._hashable_value



    def get_total_volume(self: Well) -> float:
        """Total volume present in the well."""
        return sum(
            [liquid_volume.volume for liquid_volume in self.liquid_volumes.values()],
        )

    def aspirate(self: Well, volume: float) -> list[LiquidVolume]:
        """Aspirate a volume from the well. Returns a list of (liquid,volume) that was aspirated."""
        aspirated_liquids: list[LiquidVolume] = []

        total_volume = self.get_total_volume()

        if volume > total_volume:
            msg = "You are removing more liquid than is available in the wells. This is weird."
            raise ValueError(msg)

        removed_fraction = volume / total_volume

        for key, liquid_volume in self.liquid_volumes.items():
            removed_volume = liquid_volume.volume * removed_fraction
            new_volume = liquid_volume.volume - removed_volume

            aspirated_liquids.append(LiquidVolume(liquid_volume.liquid, removed_volume))

            if new_volume > 0:
                self.liquid_volumes[key] = LiquidVolume(liquid_volume.liquid, new_volume)
            else:
                del self.liquid_volumes[key]

        return aspirated_liquids

    def dispense(self: Well, liquid_volumes: list[LiquidVolume]) -> None:
        """Dispense a list of (liquid,volume) into a well."""
        for dispensed_liquid_volume in liquid_volumes:

            name = dispensed_liquid_volume.liquid.name

            current_volume = 0
            if name in self.liquid_volumes:
                current_volume = self.liquid_volumes[name].volume

            self.liquid_volumes[name] = LiquidVolume(
                dispensed_liquid_volume.liquid,
                dispensed_liquid_volume.volume + current_volume,
            )

    def get_well_property(
        self: Well,
        property_function: Callable[[Liquid], PropertyWeight[T]],
    ) -> T:
        """Get a specific liquid property based on the composition of liquids in the well."""
        if len(self.liquid_volumes) == 0:
            msg = "Well is empty."
            raise ValueError(msg)

        property_volumes = [
            PropertyWeightVolume(property_function(liquid_volume.liquid), liquid_volume.volume)
            for liquid_volume in self.liquid_volumes.values()
        ]

        return cast(T,cast(LiquidPropertyBase,property_volumes[0].property_weight.property).calculate_composition_property(
            property_volumes,
        ))

