from dataclasses import field
from typing import cast

from pydantic import dataclasses

from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import (
    Channel1000uLCOREGrip as COREGripperDriver,
)
from PytomatedLiquidHandling.HAL import LayoutItem, DeckLocation

from .Base import TransportABC


@dataclasses.dataclass(kw_only=True)
class HamiltonCOREGripper(TransportABC):
    Backend: Backend.HamiltonBackendABC
    GripperLabwareID: str

    @dataclasses.dataclass(kw_only=True)
    class PickupOptions(TransportABC.PickupOptions):
        """Options to pick up labware from deck location"""

        ...

    @dataclasses.dataclass(kw_only=True)
    class DropoffOptions(TransportABC.DropoffOptions):
        """Options to drop off labware to deck location"""

        CheckPlateExists: COREGripperDriver.PlacePlate.Options.YesNoOptions = field(
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

        GetPlateOptionsInstance = COREGripperDriver.GetPlate.Options(
            GripperLabwareID=self.GripperLabwareID,
            PlateLabwareID=SourceLayoutItem.LabwareID,
            GripWidth=Labware.Dimensions.YLength - Labware.TransportOffsets.Close,
            OpenWidth=Labware.Dimensions.YLength + Labware.TransportOffsets.Open,
            GripHeight=Labware.TransportOffsets.Top,
        )

        CommandInstance = COREGripperDriver.GetPlate.Command(
            Options=GetPlateOptionsInstance,
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(CommandInstance, COREGripperDriver.GetPlate.Response)

        DropoffOptions = cast(
            HamiltonCOREGripper.DropoffOptions,
            CompatibleConfigs[1].DropoffOptions,
        )

        CommandInstance = COREGripperDriver.PlacePlate.Command(
            Options=COREGripperDriver.PlacePlate.Options(
                LabwareID=DestinationLayoutItem.LabwareID,
                CheckPlateExists=DropoffOptions.CheckPlateExists,
                EjectTool=COREGripperDriver.PlacePlate.Options.YesNoOptions(
                    int(self._LastTransportFlag)
                ),
            ),
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(CommandInstance, COREGripperDriver.PlacePlate.Response)

    def TransportTime(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ) -> float:
        return 0
