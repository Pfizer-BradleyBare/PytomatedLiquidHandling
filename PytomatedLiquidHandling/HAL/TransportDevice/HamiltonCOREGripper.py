from ...Driver.Hamilton.Transport import COREGripper as COREGripperDriver
from .BaseTransportDevice import TransportOptions
from .BaseTransportDevice import TransportDevice
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from dataclasses import dataclass


@dataclass
class HamiltonCOREGripper(TransportDevice):
    BackendInstance: HamiltonBackendABC
    GripperToolSequence: str

    def Initialize(
        self,
    ):
        ...

    def Deinitialize(
        self,
    ):
        ...

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        self._CheckIsValid(TransportOptionsInstance)

        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        SourceTransportableLabware = (
            self.TransportableLabwareTrackerInstance.GetObjectByName(
                SourceLayoutItem.LabwareInstance.GetUniqueIdentifier()
            )
        )

        GetPlateOptionsInstance = COREGripperDriver.GetPlate.Options(
            GripperSequence=self.GripperToolSequence,
            PlateSequence=SourceLayoutItem.Sequence,
            GripWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            - SourceTransportableLabware.TransportParametersInstance.CloseOffset,
            OpenWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            + SourceTransportableLabware.TransportParametersInstance.OpenOffset,
            GripHeight=SourceTransportableLabware.TransportParametersInstance.PickupHeight,
        )

        try:
            CommandInstance = COREGripperDriver.GetPlate.Command(
                OptionsInstance=GetPlateOptionsInstance,
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            self.BackendInstance.GetResponse(CommandInstance, CommandInstance.Response)

        except:
            ...

        try:
            CommandInstance = COREGripperDriver.PlacePlate.Command(
                OptionsInstance=COREGripperDriver.PlacePlate.Options(
                    PlateSequence=DestinationLayoutItem.Sequence,
                    CheckPlateExists=DestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.HomePlaceConfig[
                        "CheckPlateExists"
                    ],
                    EjectTool=COREGripperDriver.PlacePlate.Options.YesNoOptions(
                        self._LastTransportFlag
                    ),
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            self.BackendInstance.GetResponse(CommandInstance, CommandInstance.Response)

        except:
            ...

    def GetGetConfigKeys(self) -> list[str]:
        ...

    def GetPlaceConfigKeys(self) -> list[str]:
        return ["CheckPlateExists"]
