from dataclasses import field

from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import (
    Channel1000uLCOREGrip as COREGripperDriver,
)
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TransportABC


class HamiltonCOREGripper(TransportABC):
    GripperLabwareID: str

    @dataclass
    class PickupOptions(TransportABC.PickupOptions):
        ...

    @dataclass
    class DropoffOptions(TransportABC.DropoffOptions):
        CheckPlateExists: COREGripperDriver.PlacePlate.Options.YesNoOptions = field(
            init=True, compare=False
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

        GetPlateOptionsInstance = COREGripperDriver.GetPlate.Options(
            GripperLabwareID=self.GripperLabwareID,
            PlateLabwareID=SourceLayoutItem.LabwareID,
            GripWidth=Labware.Dimensions.YLength - Labware.TransportOffsets.Close,
            OpenWidth=Labware.Dimensions.YLength + Labware.TransportOffsets.Open,
            GripHeight=Labware.TransportOffsets.Top,
        )

        CommandInstance = COREGripperDriver.GetPlate.Command(
            Options=GetPlateOptionsInstance,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(CommandInstance, COREGripperDriver.GetPlate.Response)

        DropoffOptions = (
            DestinationLayoutItem.DeckLocation.TransportConfig.DropoffOptions
        )

        if not isinstance(DropoffOptions, self.DropoffOptions):
            raise Exception("This should never happen")

        CommandInstance = COREGripperDriver.PlacePlate.Command(
            Options=COREGripperDriver.PlacePlate.Options(
                LabwareID=DestinationLayoutItem.LabwareID,
                CheckPlateExists=DropoffOptions.CheckPlateExists,
                EjectTool=COREGripperDriver.PlacePlate.Options.YesNoOptions(
                    int(self._LastTransportFlag)
                ),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
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
