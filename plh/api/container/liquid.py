from __future__ import annotations

from dataclasses import dataclass, field

from .property import Homogeneity, Polarity, Viscosity, Volatility


@dataclass(frozen=True)
class Liquid:
    """A representation of a liquid in a physical well.
    A liquid will be described by a name and physical properties. For now a liquid is defined as having 4 properties:
    ```Volatility```, ```Viscosity```, ```Homogeneity```,and ```Polarity```.
    """

    def __hash__(self: Liquid) -> int:
        return hash(
            f"{self.volatility[0].value}{self.volatility[1]}"
            f"{self.viscosity[0].value}{self.viscosity[1]}"
            f"{self.homogeneity[0].value}{self.homogeneity[1]}"
            f"{self.polarity[0].value}{self.polarity[1]}",
        )
        # The hash is the value plus the weight of each property concatenated into a string.

    def __eq__(self: Liquid, __value: Liquid) -> bool:
        return hash(self) == hash(__value)

    volatility: tuple[Volatility, int] = field(
        default=(Volatility.MEDIUM, 1),
    )
    """The voltaility property and weight for the liquid.
    For example: ACN mixed with water still makes a solution significantly non-viscous but only slightly volatile."""

    viscosity: tuple[Viscosity, int] = field(
        default=(Viscosity.MEDIUM, 1),
    )
    """The viscosity property and weight for the liquid.
    For example: ACN mixed with water still makes a solution significantly non-viscous but only slightly volatile."""

    homogeneity: tuple[Homogeneity, int] = field(
        default=(Homogeneity.HOMOGENOUS, 1),
    )
    """The homogeneity property and weight for the liquid.
    For example: It's possible to have a reagent that causes a precipitation.
    A small amount of reagent added would have to have a huge weight to change the composition."""

    polarity: tuple[Polarity, int] = field(default=(Polarity.POLAR, 1))
    """The polarity property and weight for the liquid.
    For example: Chloroform is not conductive at all. But a small amount of water will add significant polarity."""
