from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Hamilton.Backend.BaseHamiltonBackend import (
    HamiltonBackendABC,
)
from PytomatedLiquidHandling.Driver.Hamilton.Transport import IPG as IPGDriver
from .Base import TransportDeviceABC, TransportOptions
from PytomatedLiquidHandling.HAL import DeckLocation


@dataclass
class HamiltonInternalPlateGripper(TransportDeviceABC):
    BackendInstance: HamiltonBackendABC

    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
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

    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        Movement: IPGDriver.PlacePlate.Options.MovementOptions = field(
            init=False, compare=True
        )
        RetractDistance: float = field(init=False, compare=False)
        LiftupHeight: float = field(init=False, compare=False)
        LabwareOrientation: IPGDriver.PlacePlate.Options.LabwareOrientationOptions = (
            field(init=False, compare=True)
        )

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        if (
            SourceLayoutItem.DeckLocation.TransportConfig.HomePickupOptions
            != DestinationLayoutItem.DeckLocation.TransportConfig.AwayPickupOptions
        ):
            raise Exception(
                "Source and destination transport configuration is not compatible."
            )

        if SourceLayoutItem.Labware != DestinationLayoutItem.Labware:
            raise Exception("Source and destination labware are not compatible")

        if SourceLayoutItem.DeckLocation == DestinationLayoutItem.DeckLocation:
            return

        Labware = SourceLayoutItem.Labware

        PickupOptions = SourceLayoutItem.DeckLocation.TransportConfig.HomePickupOptions

        if not isinstance(PickupOptions, self.PickupOptions):
            raise Exception("This should never happen")

        CommandInstance = IPGDriver.GetPlate.Command(
            Options=IPGDriver.GetPlate.Options(
                PlateSequence=SourceLayoutItem.Sequence,
                GripWidth=Labware.Dimensions.ShortSide - Labware.TransportOffsets.Close,
                OpenWidth=Labware.Dimensions.ShortSide + Labware.TransportOffsets.Open,
                GripHeight=Labware.TransportOffsets.BottomOffset,
                GripMode=PickupOptions.GripMode,
                Movement=PickupOptions.Movement,
                RetractDistance=PickupOptions.RetractDistance,
                LiftupHeight=PickupOptions.LiftupHeight,
                LabwareOrientation=PickupOptions.LabwareOrientation,
                InverseGrip=PickupOptions.InverseGrip,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, IPGDriver.GetPlate.Response)

        DropoffOptions = (
            DestinationLayoutItem.DeckLocation.TransportConfig.HomeDropoffOptions
        )

        if not isinstance(DropoffOptions, self.DropoffOptions):
            raise Exception("This should never happen")

        CommandInstance = IPGDriver.PlacePlate.Command(
            Options=IPGDriver.PlacePlate.Options(
                PlateSequence=DestinationLayoutItem.Sequence,
                Movement=DropoffOptions.Movement,
                RetractDistance=DropoffOptions.RetractDistance,
                LiftupHeight=DropoffOptions.LiftupHeight,
                LabwareOrientation=DropoffOptions.LabwareOrientation,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, IPGDriver.PlacePlate.Response)
