from __future__ import annotations

from typing import Annotated, cast

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.device.HAMILTON.ML_STAR import Autoload
from plh.implementation import backend
from plh.implementation import carrier as c

from .carrier_loader_base import CarrierLoaderBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVantageAutoload(CarrierLoaderBase):
    """A device that can move a carrier in and out of a system without user intervention."""

    backend: Annotated[
        VantageTrackGripperEntryExit,
        BeforeValidator(backend.validate_instance),
    ]
    supported_carriers: Annotated[
        list[c.MoveableCarrier],
        BeforeValidator(c.validate_list),
    ]

    def initialize(self: HamiltonVantageAutoload) -> None:
        """No initialization required."""

    def deinitialize(self: HamiltonVantageAutoload) -> None:
        """No deinitialization required."""

    def load(
        self: CarrierLoaderBase,
        carrier: c.CarrierBase,
    ) -> list[tuple[int, str]]:
        """Uses the autoload to load carriers into the deck. Will read barcode of loaded positions if barcode is available then return [(position,barcode),...]."""
        carrier = cast(c.HamiltonAutoloadCarrier, carrier)

        command = Autoload.LoadCarrier.Command(
            backend_error_handling=False,
            options=Autoload.LoadCarrier.Options(LabwareID=carrier.carrier_labware_id),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(command, Autoload.LoadCarrier.Response)

        return []

    def unload(self: CarrierLoaderBase, carrier: c.CarrierBase) -> None:
        """Uses the autoload to unload carriers."""
        carrier = cast(c.HamiltonAutoloadCarrier, carrier)

        command = Autoload.UnloadCarrier.Command(
            backend_error_handling=False,
            options=Autoload.UnloadCarrier.Options(
                LabwareID=carrier.carrier_labware_id,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Autoload.UnloadCarrier.Response)
