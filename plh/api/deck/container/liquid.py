from __future__ import annotations

from dataclasses import dataclass, field

from .property import Homogeneity, Polarity, PropertyWeight, Viscosity, Volatility


@dataclass(frozen=True)
class LiquidVolume:
    """A volume of a given liquid."""

    liquid: Liquid
    """The ```Liquid```."""

    volume: float
    """The volume of the ```Liquid```."""


@dataclass(frozen=True)
class Liquid:
    """A representation of a liquid in a physical well.
    A liquid will be described by a name and physical properties. For now a liquid is defined as having 4 properties:
    ```Volatility```, ```Viscosity```, ```Homogeneity```,and ```Polarity```.
    """

    def __hash__(self:Liquid) -> int:
        return hash(self.name)

    def __eq__(self:Liquid, __value: Liquid) -> bool:
        return self.name == __value.name

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

