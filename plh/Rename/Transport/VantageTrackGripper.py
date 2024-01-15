from dataclasses import field
from typing import cast

from pydantic import dataclasses

from PytomatedLiquidHandling.Driver.Hamilton import ML_STAR, Backend, TrackGripper
from PytomatedLiquidHandling.HAL import LayoutItem, DeckLocation

from .Base import TransportABC


@dataclasses.dataclass(kw_only=True)
class VantageTrackGripper(TransportABC):
    Backend: Backend.VantageTrackGripperEntryExit

    @dataclasses.dataclass(kw_only=True)
    class PickupOptions(TransportABC.PickupOptions):
        """Options to pick up labware from deck location
        NOTE: Pickup and Dropoff TaughtPathName should be same due to how track gripper works
        """

        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        Orientation: ML_STAR.iSwap.GetPlate.Options.LabwareOrientationOptions = field(
            compare=True
        )
        CoordinatedMovement: TrackGripper.GripPlateFromTaughtPosition.Options.YesNoOptions = field(
            compare=False
        )

    @dataclasses.dataclass(kw_only=True)
    class DropoffOptions(TransportABC.DropoffOptions):
        """Options to drop off labware to deck location
        NOTE: Pickup and Dropoff TaughtPathName and PathTime should be same due to how track gripper works
        """

        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        CoordinatedMovement: TrackGripper.PlacePlateToTaughtPosition.Options.YesNoOptions = field(
            compare=False
        )

    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        if SourceLayoutItem.DeckLocation == DestinationLayoutItem.DeckLocation:
            return

        CompatibleConfigs = (
            DeckLocation.TransportableDeckLocation.GetCompatibleTransportConfigs(
                SourceLayoutItem.DeckLocation,
                DestinationLayoutItem.DeckLocation,
            )[0]
        )

        Labware = SourceLayoutItem.Labware

        PickupOptions = cast(
            VantageTrackGripper.PickupOptions,
            CompatibleConfigs[0].PickupOptions,
        )

        if (
            PickupOptions.Orientation
            == ML_STAR.iSwap.GetPlate.Options.LabwareOrientationOptions.PositiveYAxis
        ):
            OpenWidth = Labware.Dimensions.XLength + Labware.TransportOffsets.Open
        else:
            OpenWidth = Labware.Dimensions.YLength + Labware.TransportOffsets.Open

        CommandInstance = TrackGripper.GripPlateFromTaughtPosition.Command(
            Options=TrackGripper.GripPlateFromTaughtPosition.Options(
                OpenWidth=OpenWidth,
                CoordinatedMovement=PickupOptions.CoordinatedMovement,
                GripForcePercentage=100,
                SpeedPercentage=100,
                CollisionControl=TrackGripper.GripPlateFromTaughtPosition.Options.YesNoOptions.Yes,
                TaughtPathName=PickupOptions.TaughtPathName,
            ),
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(
            CommandInstance, TrackGripper.GripPlateFromTaughtPosition.Response
        )

        DropoffOptions = cast(
            VantageTrackGripper.DropoffOptions,
            CompatibleConfigs[1].DropoffOptions,
        )

        CommandInstance = TrackGripper.PlacePlateToTaughtPosition.Command(
            Options=TrackGripper.PlacePlateToTaughtPosition.Options(
                OpenWidth=Labware.TransportOffsets.Open,
                TaughtPathName=DropoffOptions.TaughtPathName,
                CoordinatedMovement=DropoffOptions.CoordinatedMovement,
                SpeedPercentage=100,
                CollisionControl=TrackGripper.PlacePlateToTaughtPosition.Options.YesNoOptions.Yes,
            ),
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(
            CommandInstance, TrackGripper.PlacePlateToTaughtPosition.Response
        )

    def TransportTime(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ) -> float:
        return 0
