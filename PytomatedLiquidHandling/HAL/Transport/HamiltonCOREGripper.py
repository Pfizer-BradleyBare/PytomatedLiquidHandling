from dataclasses import field
from typing import cast

from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import (
    Channel1000uLCOREGrip as COREGripperDriver,
)
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TransportABC


class HamiltonCOREGripper(TransportABC):
    Backend: Backend.HamiltonBackendABC
    GripperLabwareID: str

    @dataclass
    class PickupOptions(TransportABC.PickupOptions):
        """Options to pick up labware from deck location"""

        ...

    @dataclass
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
            DestinationLayoutItem.DeckLocation.TransportConfig.DropoffOptions,
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
