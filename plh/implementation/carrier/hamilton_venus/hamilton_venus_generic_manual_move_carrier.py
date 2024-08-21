from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from plh.device.HAMILTON.backend import HamiltonBackendBase
from plh.implementation import backend, deck

from ..manual_move_liquid_handler_carrier_base import ManualMoveLiquidHandlerCarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusGenericManualMoveCarrier(ManualMoveLiquidHandlerCarrierBase):
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

    def initialize(self: HamiltonVenusGenericManualMoveCarrier) -> None:
        return super().initialize()

    def deinitialize(self: HamiltonVenusGenericManualMoveCarrier) -> None:
        return super().deinitialize()
