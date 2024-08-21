from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from plh.implementation import deck

from ..stationary_liquid_handler_carrier_base import StationaryLiquidHandlerCarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusGenericStationaryCarrier(StationaryLiquidHandlerCarrierBase):
    """A physical carrier on a system deck."""

    deck: Annotated[
        deck.hamilton_venus.HamiltonDeckBase,
        BeforeValidator(deck.validate_instance),
    ]
    """A deck object."""
