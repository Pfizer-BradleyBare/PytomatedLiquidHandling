from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Hamilton.Backend.BaseHamiltonBackend import (
    HamiltonBackendABC,
)
from PytomatedLiquidHandling.Driver.Hamilton.Transport import (
    COREGripper as COREGripperDriver,
)
from .Base import TransportDeviceABC, TransportOptions
from PytomatedLiquidHandling.HAL import DeckLocation


@dataclass
class HamiltonCOREGripper(TransportDeviceABC):
    BackendInstance: HamiltonBackendABC
    GripperToolSequence: str

    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        CheckPlateExists: COREGripperDriver.PlacePlate.Options.YesNoOptions = field(
            init=False, compare=False
        )

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

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
            GripperSequence=self.GripperToolSequence,
            PlateSequence=SourceLayoutItem.Sequence,
            GripWidth=Labware.Dimensions.ShortSide - Labware.TransportOffsets.Close,
            OpenWidth=Labware.Dimensions.ShortSide + Labware.TransportOffsets.Open,
            GripHeight=Labware.TransportOffsets.BottomOffset,
        )

        CommandInstance = COREGripperDriver.GetPlate.Command(
            Options=GetPlateOptionsInstance,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(
            CommandInstance, COREGripperDriver.GetPlate.Response
        )

        DropoffOptions = (
            DestinationLayoutItem.DeckLocation.TransportConfig.DropoffOptions
        )

        if not isinstance(DropoffOptions, self.DropoffOptions):
            raise Exception("This should never happen")

        CommandInstance = COREGripperDriver.PlacePlate.Command(
            Options=COREGripperDriver.PlacePlate.Options(
                PlateSequence=DestinationLayoutItem.Sequence,
                CheckPlateExists=DropoffOptions.CheckPlateExists,
                EjectTool=COREGripperDriver.PlacePlate.Options.YesNoOptions(
                    int(self._LastTransportFlag)
                ),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(
            CommandInstance, COREGripperDriver.PlacePlate.Response
        )
