from __future__ import annotations

from dataclasses import field
from typing import Annotated, cast

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON import ML_STAR, TrackGripper
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal import backend, deck_location
from plh.hal.exceptions import CriticalHALError

from .options import GetPlaceOptions
from .transport_base import *
from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True, eq=False)
class VantageTrackGripper(TransportBase):

    backend: Annotated[
        VantageTrackGripperEntryExit,
        BeforeValidator(backend.validate_instance),
    ]

    @dataclasses.dataclass(kw_only=True)
    class GetOptions(TransportBase.GetOptions):
        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        Orientation: ML_STAR.iSwap.GetPlate.LabwareOrientationOptions = field(
            compare=True,
        )
        CoordinatedMovement: TrackGripper.GripPlateFromTaughtPosition.YesNoOptions = (
            field(
                compare=False,
            )
        )

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions(TransportBase.PlaceOptions):
        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        CoordinatedMovement: TrackGripper.PlacePlateToTaughtPosition.YesNoOptions = (
            field(
                compare=False,
            )
        )

    def get(
        self: VantageTrackGripper,
        options: GetPlaceOptions,
    ) -> None:
        self.assert_supported_labware(
            options.source_layout_item.labware,
            options.destination_layout_item.labware,
        )
        self.assert_supported_deck_locations(
            options.source_layout_item.deck_location,
            options.destination_layout_item.deck_location,
        )
        self.assert_compatible_deck_locations(
            options.source_layout_item.deck_location,
            options.destination_layout_item.deck_location,
        )

        source_layout_item = options.source_layout_item
        destination_layout_item = options.destination_layout_item

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source_layout_item.deck_location,
                destination_layout_item.deck_location,
            )[0]
        )

        labware = source_layout_item.labware

        get_options = cast(
            VantageTrackGripper.GetOptions,
            compatible_configs[0].get_options,
        )

        if (
            get_options.Orientation
            == ML_STAR.iSwap.GetPlate.LabwareOrientationOptions.PositiveYAxis
        ):
            open_width = labware.dimensions.x_length + labware.transport_offsets.open
        else:
            open_width = labware.dimensions.y_length + labware.transport_offsets.open

        command = TrackGripper.GripPlateFromTaughtPosition.Command(
            options=TrackGripper.GripPlateFromTaughtPosition.Options(
                OpenWidth=open_width,
                CoordinatedMovement=get_options.CoordinatedMovement,
                GripForcePercentage=100,
                SpeedPercentage=100,
                CollisionControl=TrackGripper.GripPlateFromTaughtPosition.YesNoOptions.Yes,
                TaughtPathName=get_options.TaughtPathName,
            ),
            backend_error_handling=False,
        )

        try:
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                TrackGripper.GripPlateFromTaughtPosition.Response,
            )
        except* TrackGripper.GripPlateFromTaughtPosition.exceptions.HardwareError as e:
            raise ExceptionGroup("Exception", [CriticalHALError(self)]) from e

    def get_time(
        self: VantageTrackGripper,
        options: GetPlaceOptions,
    ) -> float: ...

    def place(
        self: VantageTrackGripper,
        options: GetPlaceOptions,
    ) -> None:
        self.assert_supported_labware(
            options.source_layout_item.labware,
            options.destination_layout_item.labware,
        )
        self.assert_supported_deck_locations(
            options.source_layout_item.deck_location,
            options.destination_layout_item.deck_location,
        )
        self.assert_compatible_deck_locations(
            options.source_layout_item.deck_location,
            options.destination_layout_item.deck_location,
        )

        source_layout_item = options.source_layout_item
        destination_layout_item = options.destination_layout_item

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source_layout_item.deck_location,
                destination_layout_item.deck_location,
            )[0]
        )

        labware = destination_layout_item.labware

        place_options = cast(
            VantageTrackGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        command = TrackGripper.PlacePlateToTaughtPosition.Command(
            options=TrackGripper.PlacePlateToTaughtPosition.Options(
                OpenWidth=labware.transport_offsets.open,
                TaughtPathName=place_options.TaughtPathName,
                CoordinatedMovement=place_options.CoordinatedMovement,
                SpeedPercentage=100,
                CollisionControl=TrackGripper.PlacePlateToTaughtPosition.YesNoOptions.Yes,
            ),
            backend_error_handling=False,
        )

        try:
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                TrackGripper.PlacePlateToTaughtPosition.Response,
            )
        except* TrackGripper.PlacePlateToTaughtPosition.exceptions.HardwareError as e:
            raise ExceptionGroup("Exception", [CriticalHALError(self)]) from e

    def place_time(
        self: VantageTrackGripper,
        options: GetPlaceOptions,
    ) -> float: ...
