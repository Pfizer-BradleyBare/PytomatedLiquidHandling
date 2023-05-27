from ...Driver.Hamilton.Transport import Gripper as GripperDriver
from .BaseTransportDevice import Options, OptionsTracker
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

    def Transport(self, OptionsInstance: Options):
        if not SourceLayoutItem.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.IsTracked(
            type(self).__name__
        ):
            raise Exception(
                "This transport device is not supported for this source deck location"
            )

        if not DestinationLayoutItem.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.IsTracked(
            type(self).__name__
        ):
            raise Exception(
                "This transport device is not supported for this source deck location"
            )
        # Check that this is a supported transport device for the deck locations

        SourceLabwareInstance = SourceLayoutItem.LabwareInstance
        DestinationLabwareInstance = DestinationLayoutItem.LabwareInstance

        if (
            SourceLabwareInstance.GetUniqueIdentifier()
            != DestinationLabwareInstance.GetUniqueIdentifier()
        ):
            raise Exception(
                "Your source and destination labware are not the same... How did this happen???"
            )
        # Check that the labware is the same for both source and destination

        if not self.TransportableLabwareTrackerInstance.IsTracked(
            SourceLabwareInstance.GetUniqueIdentifier()
        ):
            raise Exception("The labware is not supported by this transport device")
        # Check that the transport device can move this labware

        SourceTransportableLabware = (
            self.TransportableLabwareTrackerInstance.GetObjectByName(
                SourceLabwareInstance.GetUniqueIdentifier()
            )
        )

        GetPlateOptionsInstance = GripperDriver.GetPlate.Options(
            self.GripperToolSequence,
            SourceLayoutItem.Sequence,
            SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            - SourceTransportableLabware.TransportParametersInstance.CloseOffset,
            SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            + SourceTransportableLabware.TransportParametersInstance.OpenOffset,
        )
        GetPlateOptionsInstance.GripHeight = (
            SourceTransportableLabware.TransportParametersInstance.PickupHeight
        )

        try:
            GripperDriver.GetPlate.Command(GetPlateOptionsInstance, True).Execute()

        except:
            ...

        try:
            GripperDriver.PlacePlate.Command(
                GripperDriver.PlacePlate.Options(
                    DestinationLayoutItem.Sequence,
                ),
                True,
            ).Execute()

        except:
            ...

    def GetConfigKeys(self) -> list[str]:
        return []
