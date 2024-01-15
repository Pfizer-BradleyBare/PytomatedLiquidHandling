from dataclasses import field
from typing import cast

from pydantic import dataclasses
from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import iSwap as IPGDriver

from plh.hal import DeckLocation, LayoutItem

from .Base import TransportBase


@dataclasses.dataclass(kw_only=True)
class HamiltonInternalPlateGripper(TransportBase):
    Backend: Backend.HamiltonBackendABC

    @dataclasses.dataclass(kw_only=True)
    class PickupOptions(TransportBase.PickupOptions):
        """Options to pick up labware from deck location"""

        GripMode: IPGDriver.GetPlate.Options.GripModeOptions = field(compare=True)
        Movement: IPGDriver.GetPlate.Options.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: IPGDriver.GetPlate.Options.LabwareOrientationOptions = (
            field(compare=True)
        )
        InverseGrip: IPGDriver.GetPlate.Options.YesNoOptions = field(compare=True)

    @dataclasses.dataclass(kw_only=True)
    class DropoffOptions(TransportBase.DropoffOptions):
        """Options to drop off labware to deck location"""

        Movement: IPGDriver.PlacePlate.Options.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: IPGDriver.PlacePlate.Options.LabwareOrientationOptions = (
            field(compare=True)
        )

    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemBase,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemBase,
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
            HamiltonInternalPlateGripper.PickupOptions,
            CompatibleConfigs[0].PickupOptions,
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
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(CommandInstance, IPGDriver.GetPlate.Response)

        DropoffOptions = cast(
            HamiltonInternalPlateGripper.DropoffOptions,
            CompatibleConfigs[1].DropoffOptions,
        )

        CommandInstance = IPGDriver.PlacePlate.Command(
            Options=IPGDriver.PlacePlate.Options(
                LabwareID=DestinationLayoutItem.LabwareID,
                Movement=DropoffOptions.Movement,
                RetractDistance=DropoffOptions.RetractDistance,
                LiftupHeight=DropoffOptions.LiftupHeight,
                LabwareOrientation=DropoffOptions.LabwareOrientation,
            ),
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(CommandInstance, IPGDriver.PlacePlate.Response)

    def TransportTime(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemBase,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemBase,
    ) -> float:
        return 0
