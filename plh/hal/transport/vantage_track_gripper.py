from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, cast

from pydantic import dataclasses

from plh.driver.HAMILTON import ML_STAR, TrackGripper
from plh.hal import deck_location, layout_item

from .transport_base import TransportBase

if TYPE_CHECKING:
    from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit


@dataclasses.dataclass(kw_only=True)
class VantageTrackGripper(TransportBase):
    backend: VantageTrackGripperEntryExit

    @dataclasses.dataclass(kw_only=True)
    class PickupOptions(TransportBase.PickupOptions):
        """Options to pick up labware from deck location
        NOTE: Pickup and Dropoff TaughtPathName should be same due to how track gripper works
        """

        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        Orientation: ML_STAR.iSwap.GetPlate.Options.LabwareOrientationOptions = field(
            compare=True,
        )
        CoordinatedMovement: TrackGripper.GripPlateFromTaughtPosition.Options.YesNoOptions = field(
            compare=False,
        )

    @dataclasses.dataclass(kw_only=True)
    class DropoffOptions(TransportBase.DropoffOptions):
        """Options to drop off labware to deck location
        NOTE: Pickup and Dropoff TaughtPathName and PathTime should be same due to how track gripper works
        """

        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        CoordinatedMovement: TrackGripper.PlacePlateToTaughtPosition.Options.YesNoOptions = field(
            compare=False,
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

        pickup_options = cast(
            VantageTrackGripper.PickupOptions,
            compatible_configs[0].pickup_options,
        )

        if (
            pickup_options.Orientation
            == ML_STAR.iSwap.GetPlate.Options.LabwareOrientationOptions.PositiveYAxis
        ):
            open_width = labware.dimensions.x_length + labware.transport_offsets.open
        else:
            open_width = labware.dimensions.y_length + labware.transport_offsets.open

        command = TrackGripper.GripPlateFromTaughtPosition.Command(
            options=TrackGripper.GripPlateFromTaughtPosition.Options(
                OpenWidth=open_width,
                CoordinatedMovement=pickup_options.CoordinatedMovement,
                GripForcePercentage=100,
                SpeedPercentage=100,
                CollisionControl=TrackGripper.GripPlateFromTaughtPosition.Options.YesNoOptions.Yes,
                TaughtPathName=pickup_options.TaughtPathName,
            ),
            backend_error_handling=self.backend_error_handling,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            TrackGripper.GripPlateFromTaughtPosition.Response,
        )

        dropoff_options = cast(
            VantageTrackGripper.DropoffOptions,
            compatible_configs[1].dropoff_options,
        )

        command = TrackGripper.PlacePlateToTaughtPosition.Command(
            options=TrackGripper.PlacePlateToTaughtPosition.Options(
                OpenWidth=labware.transport_offsets.open,
                TaughtPathName=dropoff_options.TaughtPathName,
                CoordinatedMovement=dropoff_options.CoordinatedMovement,
                SpeedPercentage=100,
                CollisionControl=TrackGripper.PlacePlateToTaughtPosition.Options.YesNoOptions.Yes,
            ),
            backend_error_handling=self.backend_error_handling,
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
