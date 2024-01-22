from __future__ import annotations

from dataclasses import field
from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON import ML_STAR, TrackGripper
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal import deck_location, layout_item

from .transport_base import *
from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True)
class VantageTrackGripper(TransportBase):
    backend: VantageTrackGripperEntryExit

    @dataclasses.dataclass(kw_only=True)
    class GetOptions(TransportBase.GetOptions):
        """Options to pick up labware from deck location
        NOTE: Pickup and Dropoff TaughtPathName should be same due to how track gripper works
        """

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
        """Options to drop off labware to deck location
        NOTE: Pickup and Dropoff TaughtPathName and PathTime should be same due to how track gripper works
        """

        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        CoordinatedMovement: TrackGripper.PlacePlateToTaughtPosition.YesNoOptions = (
            field(
                compare=False,
            )
        )

    def transport(
        self: VantageTrackGripper,
        source_layout_item: layout_item.LayoutItemBase,
        destination_layout_item: layout_item.LayoutItemBase,
    ) -> None:
        if source_layout_item.deck_location == destination_layout_item.deck_location:
            return

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
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            TrackGripper.GripPlateFromTaughtPosition.Response,
        )

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
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            TrackGripper.PlacePlateToTaughtPosition.Response,
        )

    def transport_time(
        self: VantageTrackGripper,
        source_layout_item: layout_item.LayoutItemBase,
        destination_layout_item: layout_item.LayoutItemBase,
    ) -> float:
        ...
