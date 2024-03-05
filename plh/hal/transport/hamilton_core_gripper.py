from __future__ import annotations

from dataclasses import field
from typing import Annotated, cast

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uLCOREGrip
from plh.hal import backend, deck_location, layout_item

from .exceptions import GetHardwareError, PlaceHardwareError
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
        CheckPlateExists: bool = field(
            compare=False,
        )

    def transport(
        self: HamiltonCOREGripper,
        source: layout_item.LayoutItemBase,
        destination: layout_item.LayoutItemBase,
    ) -> None:

        self.assert_supported_labware(
            source.labware,
            destination.labware,
        )
        self.assert_supported_deck_locations(
            source.deck_location,
            destination.deck_location,
        )
        self.assert_compatible_deck_locations(
            source.deck_location,
            destination.deck_location,
        )

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source.deck_location,
                destination.deck_location,
            )[0]
        )

        labware = source.labware

        command = Channel1000uLCOREGrip.GetPlate.Command(
            options=Channel1000uLCOREGrip.GetPlate.Options(
                GripperLabwareID=self.gripper_labware_id,
                PlateLabwareID=source.labware_id,
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
                    [GetHardwareError(self, source)],
                ) from e

        place_options = cast(
            HamiltonCOREGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        command = Channel1000uLCOREGrip.PlacePlate.Command(
            options=Channel1000uLCOREGrip.PlacePlate.Options(
                LabwareID=destination.labware_id,
                CheckPlateExists=place_options.CheckPlateExists,
                EjectTool=self.last_transport_flag,
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
                [PlaceHardwareError(self, destination)],
            ) from e

    def transport_time(
        self: TransportBase,
        source: layout_item.LayoutItemBase,
        destination: layout_item.LayoutItemBase,
    ) -> None: ...
