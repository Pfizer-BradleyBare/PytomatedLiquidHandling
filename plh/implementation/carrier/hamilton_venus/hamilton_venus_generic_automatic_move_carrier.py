from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from plh.implementation import deck

from ..manual_move_liquid_handler_carrier_base import ManualMoveLiquidHandlerCarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusGenericAutomaticMoveCarrier(ManualMoveLiquidHandlerCarrierBase):
    """A physical carrier on a system deck."""

    deck: Annotated[
        deck.hamilton_venus.HamiltonDeckBase,
        BeforeValidator(deck.validate_instance),
    ]
    """A deck object."""

    labware_id: str
    """Carrier deck labware id."""
