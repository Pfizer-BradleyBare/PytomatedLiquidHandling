from __future__ import annotations

from dataclasses import field
from typing import Annotated, cast

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON import TrackGripper
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.driver.HAMILTON.ML_STAR.Channel1000uL import MoveToPositionSequence
from plh.hal import backend, deck_location
from plh.hal.exceptions import CriticalHALError

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
        ParkLabwareID: str = field(compare=False)
        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        Orientation: TrackGripper.LabwareOrientationOptions = field(
            compare=True,
        )
        CoordinatedMovement: bool = field(
            compare=False,
        )

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions(TransportBase.PlaceOptions):
        ParkLabwareID: str = field(compare=False)
        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        CoordinatedMovement: bool = field(
            compare=False,
        )

    def transport(
        self: TransportBase,
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
            VantageTrackGripper.GetOptions,
            compatible_configs[0].get_options,
        )

        command = MoveToPositionSequence.Command(
            options=MoveToPositionSequence.Options(
                LabwareID=get_options.ParkLabwareID,
                ZMode=MoveToPositionSequence.ZModeOptions.MaxHeight,
            ),
            backend_error_handling=False,
        )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, MoveToPositionSequence.Response)

        if (
            get_options.Orientation
            == TrackGripper.LabwareOrientationOptions.PositiveYAxis
        ):
            open_width = labware.dimensions.x_length + labware.transport_offsets.open
        else:
            open_width = labware.dimensions.y_length + labware.transport_offsets.open

        command = TrackGripper.GripPlateTaught.Command(
            options=TrackGripper.GripPlateTaught.Options(
                OpenWidth=open_width,
                CoordinatedMovement=get_options.CoordinatedMovement,
                GripForcePercentage=100,
                SpeedPercentage=100,
                CollisionControl=True,
                TaughtPathName=get_options.TaughtPathName,
            ),
            backend_error_handling=False,
        )

        try:
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                TrackGripper.GripPlateTaught.Response,
            )
        except* TrackGripper.GripPlateTaught.exceptions.HardwareError as e:
            raise ExceptionGroup("Exception", [CriticalHALError(self)]) from e

        labware = destination.labware

        place_options = cast(
            VantageTrackGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        command = MoveToPositionSequence.Command(
            options=MoveToPositionSequence.Options(
                LabwareID=place_options.ParkLabwareID,
                ZMode=MoveToPositionSequence.ZModeOptions.MaxHeight,
            ),
            backend_error_handling=False,
        )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, MoveToPositionSequence.Response)

        command = TrackGripper.PlacePlateTaught.Command(
            options=TrackGripper.PlacePlateTaught.Options(
                OpenWidth=labware.transport_offsets.open,
                TaughtPathName=place_options.TaughtPathName,
                CoordinatedMovement=place_options.CoordinatedMovement,
                SpeedPercentage=100,
                CollisionControl=True,
            ),
            backend_error_handling=False,
        )

        try:
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                TrackGripper.PlacePlateTaught.Response,
            )
        except* TrackGripper.PlacePlateTaught.exceptions.HardwareError as e:
            raise ExceptionGroup("Exception", [CriticalHALError(self)]) from e

    def transport_time(
        self: TransportBase,
        source: layout_item.LayoutItemBase,
        destination: layout_item.LayoutItemBase,
    ) -> None: ...
