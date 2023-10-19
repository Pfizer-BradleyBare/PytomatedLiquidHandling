from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Hamilton.Backend.BaseHamiltonBackend import (
    HamiltonBackendABC,
)
from PytomatedLiquidHandling.Driver.Hamilton.Transport import IPG as IPGDriver
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TransportDeviceABC


@dataclass
class HamiltonInternalPlateGripper(TransportDeviceABC):
    Backend: HamiltonBackendABC

    @dataclass
    class PickupOptions(TransportDeviceABC.PickupOptions):
        GripMode: IPGDriver.GetPlate.Options.GripModeOptions = field(
            init=False, compare=True
        )
        Movement: IPGDriver.GetPlate.Options.MovementOptions = field(
            init=False, compare=True
        )
        RetractDistance: float = field(init=False, compare=False)
        LiftupHeight: float = field(init=False, compare=False)
        LabwareOrientation: IPGDriver.GetPlate.Options.LabwareOrientationOptions = (
            field(init=False, compare=True)
        )
        InverseGrip: IPGDriver.GetPlate.Options.YesNoOptions = field(
            init=False, compare=True
        )

    @dataclass
    class DropoffOptions(TransportDeviceABC.DropoffOptions):
        Movement: IPGDriver.PlacePlate.Options.MovementOptions = field(
            init=False, compare=True
        )
        RetractDistance: float = field(init=False, compare=False)
        LiftupHeight: float = field(init=False, compare=False)
        LabwareOrientation: IPGDriver.PlacePlate.Options.LabwareOrientationOptions = (
            field(init=False, compare=True)
        )

    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        if (
            SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions
            != DestinationLayoutItem.DeckLocation.TransportConfig.PickupOptions
        ):
            raise Exception(
                "Source and destination transport configuration is not compatible."
            )

        if SourceLayoutItem.Labware != DestinationLayoutItem.Labware:
            raise Exception("Source and destination labware are not compatible")

        if SourceLayoutItem.DeckLocation == DestinationLayoutItem.DeckLocation:
            return

        Labware = SourceLayoutItem.Labware

        PickupOptions = SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions

        if not isinstance(PickupOptions, self.PickupOptions):
            raise Exception("This should never happen")

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

        DropoffOptions = (
            DestinationLayoutItem.DeckLocation.TransportConfig.DropoffOptions
        )

        if not isinstance(DropoffOptions, self.DropoffOptions):
            raise Exception("This should never happen")

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
