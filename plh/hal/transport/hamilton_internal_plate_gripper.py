from __future__ import annotations

from dataclasses import field
from typing import Annotated, cast

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import iSwap
from plh.hal import backend, deck_location

from .exceptions import GetHardwareError, PlaceHardwareError
from .transport_base import *
from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonInternalPlateGripper(TransportBase):
    """Gripper that uses the Hamilton IPG (internal plate gripper)."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only Hamilton backends."""

    @dataclasses.dataclass(kw_only=True)
    class GetOptions(TransportBase.GetOptions):
        GripMode: iSwap.GetPlate.GripModeOptions = field(compare=True)
        Movement: iSwap.GetPlate.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: iSwap.GetPlate.LabwareOrientationOptions = field(
            compare=True,
        )
        InverseGrip: iSwap.GetPlate.YesNoOptions = field(compare=True)

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions(TransportBase.PlaceOptions):
        Movement: iSwap.PlacePlate.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: iSwap.PlacePlate.LabwareOrientationOptions = field(
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

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source.deck_location,
                destination.deck_location,
            )[0]
        )

        labware = source.labware

        get_options = cast(
            HamiltonInternalPlateGripper.GetOptions,
            compatible_configs[0].get_options,
        )

        command = iSwap.GetPlate.Command(
            options=iSwap.GetPlate.Options(
                LabwareID=source.labware_id,
                GripWidth=labware.dimensions.y_length - labware.transport_offsets.close,
                OpenWidth=labware.dimensions.y_length + labware.transport_offsets.open,
                GripHeight=labware.transport_offsets.top,
                GripMode=get_options.GripMode,
                Movement=get_options.Movement,
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
            self.backend.acknowledge(command, iSwap.GetPlate.Response)
        except* iSwap.GetPlate.exceptions.HardwareError as e:
            raise ExceptionGroup(
                "Exception",
                [GetHardwareError(self, source)],
            ) from e

        place_options = cast(
            HamiltonInternalPlateGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        command = iSwap.PlacePlate.Command(
            options=iSwap.PlacePlate.Options(
                LabwareID=destination.labware_id,
                Movement=place_options.Movement,
                RetractDistance=place_options.RetractDistance,
                LiftupHeight=place_options.LiftupHeight,
                LabwareOrientation=place_options.LabwareOrientation,
            ),
            backend_error_handling=False,
        )
        try:
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(command, iSwap.PlacePlate.Response)
        except* iSwap.PlacePlate.exceptions.HardwareError as e:
            raise ExceptionGroup(
                "Exception",
                [PlaceHardwareError(self, destination)],
            ) from e

    def transport_time(
        self: TransportBase,
        source: layout_item.LayoutItemBase,
        destination: layout_item.LayoutItemBase,
    ) -> None: ...
