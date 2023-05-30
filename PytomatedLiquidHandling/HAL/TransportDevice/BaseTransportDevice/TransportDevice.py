from abc import abstractmethod
from ....Tools.AbstractClasses import UniqueObjectABC
from .Interface import TransportOptions
from .TransportableLabware.TransportableLabwareTracker import (
    TransportableLabwareTracker,
)
from ....Driver.Tools.AbstractClasses import BackendABC
from ...Tools.AbstractClasses import InterfaceABC


class TransportDevice(UniqueObjectABC, InterfaceABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: BackendABC,
        CustomErrorHandling: bool,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.TransportableLabwareTrackerInstance: TransportableLabwareTracker = (
            TransportableLabwareTrackerInstance
        )
        InterfaceABC.__init__(self, BackendInstance, CustomErrorHandling)

        self._LastTransportFlag: bool = True

    def _CheckIsValid(self, TransportOptionsInstance: TransportOptions.Options):
        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        if (
            SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.GetUniqueIdentifier()
            != self.GetUniqueIdentifier()
        ):
            raise Exception(
                "This transport device is not supported for this source deck location"
            )

        if (
            DestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.GetUniqueIdentifier()
            != self.GetUniqueIdentifier()
        ):
            raise Exception(
                "This transport device is not supported for this destination deck location"
            )
        # Check that this is a supported transport device for the deck locations

        if (
            SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig
            == DestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig
        ):
            raise Exception(
                "Source and destination extra options are not compatible. Use a transition point to properly orient."
            )
        # I am comparing away configs because the way we pickup before the transfer must be the same orientation
        # This indicates a seamless transition from source home to destination home configs

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

    @abstractmethod
    def GetGetConfigKeys(self) -> list[str]:
        ...

    @abstractmethod
    def GetPlaceConfigKeys(self) -> list[str]:
        ...

    @abstractmethod
    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...
