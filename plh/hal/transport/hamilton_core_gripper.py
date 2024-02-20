from __future__ import annotations

from dataclasses import field
from typing import Annotated, cast

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uLCOREGrip
from plh.hal import backend, deck_location

from .exceptions import GetHardwareError, PlaceHardwareError
from .options import GetPlaceOptions
from .transport_base import *
from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonCOREGripper(TransportBase):
    """Gripper that uses Hamilton CORE channels."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only Hamilton backends."""

    gripper_labware_id: str
    """Labware id to pick up the gripper from the deck."""

    @dataclasses.dataclass(kw_only=True)
    class GetOptions(TransportBase.GetOptions): ...

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions(TransportBase.PlaceOptions):
        CheckPlateExists: Channel1000uLCOREGrip.PlacePlate.YesNoOptions = field(
            compare=False,
        )

    def get(
        self: HamiltonCOREGripper,
        options: GetPlaceOptions,
    ) -> None:
        self.assert_get_place(options)

        source_layout_item = options.source_layout_item

        labware = source_layout_item.labware

        command = Channel1000uLCOREGrip.GetPlate.Command(
            options=Channel1000uLCOREGrip.GetPlate.Options(
                GripperLabwareID=self.gripper_labware_id,
                PlateLabwareID=source_layout_item.labware_id,
                GripWidth=labware.dimensions.y_length - labware.transport_offsets.close,
                OpenWidth=labware.dimensions.y_length + labware.transport_offsets.open,
                GripHeight=labware.transport_offsets.top,
            ),
            backend_error_handling=False,
        )

        while True:
            try:

                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(
                    command,
                    Channel1000uLCOREGrip.GetPlate.Response,
                )
                break

            except* (
                Channel1000uLCOREGrip.GetPlate.exceptions.ExecutionError,
                Channel1000uLCOREGrip.GetPlate.exceptions.GripperPickupError,
                Channel1000uLCOREGrip.GetPlate.exceptions.NotExecutedError,
            ):
                # skip these errors.They can be repeated without consequence
                ...

            except* Channel1000uLCOREGrip.GetPlate.exceptions.HardwareError as e:
                raise ExceptionGroup(
                    "Exceptions",
                    [GetHardwareError(self, source_layout_item)],
                ) from e

    def get_time(
        self: HamiltonCOREGripper,
        options: GetPlaceOptions,
    ) -> float: ...

    def place(
        self: HamiltonCOREGripper,
        options: GetPlaceOptions,
    ) -> None:
        self.assert_get_place(options)

        source_layout_item = options.source_layout_item
        destination_layout_item = options.destination_layout_item

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source_layout_item.deck_location,
                destination_layout_item.deck_location,
            )[0]
        )

        place_options = cast(
            HamiltonCOREGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        command = Channel1000uLCOREGrip.PlacePlate.Command(
            options=Channel1000uLCOREGrip.PlacePlate.Options(
                LabwareID=destination_layout_item.labware_id,
                CheckPlateExists=place_options.CheckPlateExists,
                EjectTool=Channel1000uLCOREGrip.PlacePlate.YesNoOptions(
                    int(self.last_transport_flag),
                ),
            ),
            backend_error_handling=False,
        )

        try:
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                Channel1000uLCOREGrip.PlacePlate.Response,
            )
        except* Channel1000uLCOREGrip.PlacePlate.exceptions.HardwareError as e:
            raise ExceptionGroup(
                "Exception",
                [PlaceHardwareError(self, destination_layout_item)],
            ) from e

    def place_time(
        self: HamiltonCOREGripper,
        options: GetPlaceOptions,
    ) -> float: ...
