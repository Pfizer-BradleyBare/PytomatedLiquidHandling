from dataclasses import field
from typing import cast

from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton import ML_STAR, Backend, TrackGripper
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TransportABC


class VantageTrackGripper(TransportABC):
    Backend: Backend.VantageTrackGripperEntryExit

    @dataclass
    class PickupOptions(TransportABC.PickupOptions):
        """Options to pick up labware from deck location
        NOTE: Pickup and Dropoff TaughtPathName should be same due to how track gripper works
        """

        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)
        Orientation: ML_STAR.iSwap.GetPlate.Options.LabwareOrientationOptions = field(
            compare=True
        )

    @dataclass
    class DropoffOptions(TransportABC.DropoffOptions):
        """Options to drop off labware to deck location
        NOTE: Pickup and Dropoff TaughtPathName should be same due to how track gripper works
        """

        TaughtPathName: str = field(compare=False)
        PathTime: float = field(compare=False)

    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        if SourceLayoutItem.DeckLocation == DestinationLayoutItem.DeckLocation:
            return

        Labware = SourceLayoutItem.Labware

        PickupOptions = cast(
            VantageTrackGripper.PickupOptions,
            SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions,
        )

        CommandInstance = IPGDriver.GetPlate.Command(
            Options=IPGDriver.GetPlate.Options(
                LabwareID=SourceLayoutItem.LabwareID,
                GripWidth=Labware.Dimensions.YLength - Labware.TransportOffsets.Close,
                OpenWidth=Labware.Dimensions.YLength + Labware.TransportOffsets.Open,
                GripHeight=Labware.TransportOffsets.Top,
                GripMode=PickupOptions.GripMode,
                Movement=PickupOptions.Movement,
                RetractDistance=PickupOptions.RetractDistance,
                LiftupHeight=PickupOptions.LiftupHeight,
                LabwareOrientation=PickupOptions.LabwareOrientation,
                InverseGrip=PickupOptions.InverseGrip,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(CommandInstance, IPGDriver.GetPlate.Response)

        DropoffOptions = cast(
            VantageTrackGripper.DropoffOptions,
            DestinationLayoutItem.DeckLocation.TransportConfig.DropoffOptions,
        )

        CommandInstance = IPGDriver.PlacePlate.Command(
            Options=IPGDriver.PlacePlate.Options(
                LabwareID=DestinationLayoutItem.LabwareID,
                Movement=DropoffOptions.Movement,
                RetractDistance=DropoffOptions.RetractDistance,
                LiftupHeight=DropoffOptions.LiftupHeight,
                LabwareOrientation=DropoffOptions.LabwareOrientation,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(CommandInstance, IPGDriver.PlacePlate.Response)

    def TransportTime(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ) -> float:
        return 0
