from dataclasses import field
from typing import cast

from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import iSwap as IPGDriver
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TransportABC


class HamiltonInternalPlateGripper(TransportABC):
    Backend: Backend.HamiltonBackendABC

    @dataclass
    class PickupOptions(TransportABC.PickupOptions):
        """Options to pick up labware from deck location"""

        GripMode: IPGDriver.GetPlate.Options.GripModeOptions = field(compare=True)
        Movement: IPGDriver.GetPlate.Options.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: IPGDriver.GetPlate.Options.LabwareOrientationOptions = (
            field(compare=True)
        )
        InverseGrip: IPGDriver.GetPlate.Options.YesNoOptions = field(compare=True)

    @dataclass
    class DropoffOptions(TransportABC.DropoffOptions):
        """Options to drop off labware to deck location"""

        Movement: IPGDriver.PlacePlate.Options.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: IPGDriver.PlacePlate.Options.LabwareOrientationOptions = (
            field(compare=True)
        )

    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        if SourceLayoutItem.DeckLocation == DestinationLayoutItem.DeckLocation:
            return

        Labware = SourceLayoutItem.Labware

        PickupOptions = cast(
            HamiltonInternalPlateGripper.PickupOptions,
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
            HamiltonInternalPlateGripper.DropoffOptions,
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
