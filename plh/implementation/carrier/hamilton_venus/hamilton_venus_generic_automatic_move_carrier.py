from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from plh.device.hamilton_venus.backend import HamiltonBackendBase
from plh.device.hamilton_venus.HSLLabwrAccess import TestLabwareIDExists
from plh.implementation import backend, deck

from ..automatic_move_liquid_handler_carrier_base import (
    AutomaticMoveLiquidHandlerCarrierBase,
)


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusGenericAutomaticMoveCarrier(AutomaticMoveLiquidHandlerCarrierBase):
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

    labware_id: str
    """Carrier deck labware id."""

    def initialize(self: HamiltonVenusGenericAutomaticMoveCarrier) -> None:
        super().initialize()

        command = TestLabwareIDExists.Command(
            options=[TestLabwareIDExists.Options(LabwareID=self.labware_id)],
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(command, TestLabwareIDExists.Response)

        if len(response.BadLabwareIDs) != 0:
            raise RuntimeError(f"labware_id does not exist for {self.identifier}")

    def deinitialize(self: HamiltonVenusGenericAutomaticMoveCarrier) -> None:
        super().deinitialize()

    def move_in(self: HamiltonVenusGenericAutomaticMoveCarrier) -> None:
        """TODO"""

    def move_out(self: HamiltonVenusGenericAutomaticMoveCarrier) -> None:
        """TODO"""
