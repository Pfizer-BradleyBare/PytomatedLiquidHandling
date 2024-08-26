from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from plh.device.hamilton_venus.backend import HamiltonBackendBase
from plh.implementation import backend, deck

from ..stationary_liquid_handler_carrier_base import StationaryLiquidHandlerCarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusGenericStationaryCarrier(StationaryLiquidHandlerCarrierBase):
    """A physical carrier on a system deck."""

    backend: Annotated[
        HamiltonBackendBase,
        BeforeValidator(backend.validate_instance),
    ]

    deck: Annotated[
        deck.hamilton_venus.HamiltonVenusDeckBase,
        BeforeValidator(deck.validate_instance),
    ]
    """A deck object."""

    def initialize(self: HamiltonVenusGenericStationaryCarrier) -> None:
        return super().initialize()

    def deinitialize(self: HamiltonVenusGenericStationaryCarrier) -> None:
        return super().deinitialize()
