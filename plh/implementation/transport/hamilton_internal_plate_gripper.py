from __future__ import annotations

from dataclasses import field
from enum import Enum
from typing import Annotated, cast

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.HAMILTON.backend import HamiltonBackendBase
from plh.device.HAMILTON.ML_STAR import iSwap
from plh.implementation import backend, carrier_location, layout_item

from .exceptions import GetHardwareError, PlaceHardwareError
from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonInternalPlateGripper(TransportBase):
    """Gripper that uses the Hamilton IPG (internal plate gripper)."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only Hamilton backends."""

    class MovementOptions(Enum):
        Carrier = "Carrier"
        Complex = "Complex"

    @dataclasses.dataclass(kw_only=True)
    class GetOptions(TransportBase.GetOptions):
        GripMode: iSwap.GripModeOptions = field(compare=True)
        Movement: HamiltonInternalPlateGripper.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: iSwap.LabwareOrientationOptions = field(
            compare=True,
        )
        InverseGrip: bool = field(compare=True)

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions(TransportBase.PlaceOptions):
        Movement: HamiltonInternalPlateGripper.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: iSwap.LabwareOrientationOptions = field(
            compare=True,
        )

    def transport(
        self: HamiltonInternalPlateGripper,
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

        compatible_configs = next(
            configs
            for configs in carrier_location.TransportableCarrierLocation.get_compatible_transport_configs(
                source.deck_location,
                destination.deck_location,
            )
            if configs[0].transport_device is self
        )
        # Select the first compatible config for this transport device.

        labware = source.labware

        get_options = cast(
            HamiltonInternalPlateGripper.GetOptions,
            compatible_configs[0].get_options,
        )

        place_options = cast(
            HamiltonInternalPlateGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        if get_options.Movement == HamiltonInternalPlateGripper.MovementOptions.Carrier:
            command = iSwap.GetPlateCarrier.Command(
                options=iSwap.GetPlateCarrier.Options(
                    LabwareID=source.labware_id,
                    GripWidth=labware.y_length - labware.transport_close_offset,
                    OpenWidth=labware.y_length + labware.transport_open_offset,
                    GripHeight=labware.transport_top_offset,
                    GripMode=get_options.GripMode,
                    InverseGrip=get_options.InverseGrip,
                ),
                backend_error_handling=False,
            )
            try:
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, iSwap.GetPlateCarrier.Response)
            except* iSwap.GetPlateCarrier.exceptions.HardwareError as e:
                raise ExceptionGroup(
                    "Exception",
                    [GetHardwareError(self, source)],
                ) from e

            command = iSwap.PlacePlateCarrier.Command(
                options=iSwap.PlacePlateCarrier.Options(
                    LabwareID=destination.labware_id,
                ),
                backend_error_handling=False,
            )
            try:
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, iSwap.PlacePlateCarrier.Response)
            except* iSwap.PlacePlateCarrier.exceptions.HardwareError as e:
                raise ExceptionGroup(
                    "Exception",
                    [PlaceHardwareError(self, destination)],
                ) from e

        elif (
            get_options.Movement == HamiltonInternalPlateGripper.MovementOptions.Complex
        ):
            command = iSwap.GetPlateComplex.Command(
                options=iSwap.GetPlateComplex.Options(
                    LabwareID=source.labware_id,
                    GripWidth=labware.y_length - labware.transport_close_offset,
                    OpenWidth=labware.y_length + labware.transport_open_offset,
                    GripHeight=labware.transport_top_offset,
                    GripMode=get_options.GripMode,
                    RetractDistance=get_options.RetractDistance,
                    LiftupHeight=get_options.LiftupHeight,
                    LabwareOrientation=get_options.LabwareOrientation,
                    InverseGrip=get_options.InverseGrip,
                ),
                backend_error_handling=False,
            )
            try:
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, iSwap.GetPlateComplex.Response)
            except* iSwap.GetPlateComplex.exceptions.HardwareError as e:
                raise ExceptionGroup(
                    "Exception",
                    [GetHardwareError(self, source)],
                ) from e

            command = iSwap.PlacePlateComplex.Command(
                options=iSwap.PlacePlateComplex.Options(
                    LabwareID=destination.labware_id,
                    RetractDistance=place_options.RetractDistance,
                    LiftupHeight=place_options.LiftupHeight,
                    LabwareOrientation=place_options.LabwareOrientation,
                ),
                backend_error_handling=False,
            )
            try:
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, iSwap.PlacePlateCarrier.Response)
            except* iSwap.PlacePlateCarrier.exceptions.HardwareError as e:
                raise ExceptionGroup(
                    "Exception",
                    [PlaceHardwareError(self, destination)],
                ) from e

    def transport_time(
        self: TransportBase,
        source: layout_item.LayoutItemBase,
        destination: layout_item.LayoutItemBase,
    ) -> None: ...
