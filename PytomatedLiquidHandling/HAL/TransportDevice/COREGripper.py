from ...Driver.Hamilton.Transport import COREGripper as COREGripperDriver
from .BaseTransportDevice import TransportOptions
from .BaseTransportDevice import TransportableLabwareTracker, TransportDevice
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class COREGripper(TransportDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
        GripperToolSequence: str,
    ):
        self.GripperToolSequence: str = GripperToolSequence
        TransportDevice.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            TransportableLabwareTrackerInstance,
        )

    def Initialize(
        self,
    ):
        ...

    def Deinitialize(
        self,
    ):
        ...

    def Transport(self, OptionsInstance: TransportOptions.Options):
        self._CheckIsValid(OptionsInstance)

        SourceLayoutItem = OptionsInstance.SourceLayoutItem
        DestinationLayoutItem = OptionsInstance.DestinationLayoutItem

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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            self.GetBackend().GetResponse(CommandInstance, CommandInstance.Response)

        except:
            ...

        try:
            COREGripperDriver.PlacePlate.Command(
                OptionsInstance=COREGripperDriver.PlacePlate.Options(
                    PlateSequence=DestinationLayoutItem.Sequence
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )

        except:
            ...

    def GetConfigKeys(self) -> list[str]:
        return ["CheckPlateExists"]
