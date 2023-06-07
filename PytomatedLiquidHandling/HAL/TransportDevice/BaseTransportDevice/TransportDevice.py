from abc import abstractmethod
from ....Tools.AbstractClasses import UniqueObjectABC
from .Interface import TransportOptions
from .TransportableLabware.TransportableLabwareTracker import (
    TransportableLabwareTracker,
)
from ...Tools.AbstractClasses import InterfaceABC
from dataclasses import dataclass, field
from ...LayoutItem import CoverablePosition, NonCoverablePosition


@dataclass
class TransportDevice(InterfaceABC, UniqueObjectABC):
    TransportableLabwareTrackerInstance: TransportableLabwareTracker
    _LastTransportFlag: bool = field(init=False, default=True)

    def _CheckIsValid(self, TransportOptionsInstance: TransportOptions.Options):
        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        if (
            SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.UniqueIdentifier
            != self.UniqueIdentifier
        ):
            raise Exception(
                "This transport device is not supported for this source deck location"
            )

        if (
            DestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.UniqueIdentifier
            != self.UniqueIdentifier
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
            SourceLabwareInstance.UniqueIdentifier
            != DestinationLabwareInstance.UniqueIdentifier
        ):
            raise Exception(
                "Your source and destination labware are not the same... How did this happen???"
            )
        # Check that the labware is the same for both source and destination

        if not self.TransportableLabwareTrackerInstance.IsTracked(
            SourceLabwareInstance.UniqueIdentifier
        ):
            raise Exception("The labware is not supported by this transport device")
        # Check that the transport device can move this labware

        if not type(SourceLayoutItem) == type(DestinationLayoutItem):
            if (
                type(SourceLayoutItem) == CoverablePosition
                and type(DestinationLayoutItem) == NonCoverablePosition
                and SourceLayoutItem.IsCovered == True
            ):
                raise Exception(
                    "Source and Destination are not compatible layout items"
                )

    @abstractmethod
    def GetGetConfigKeys(self) -> list[str]:
        ...

    @abstractmethod
    def GetPlaceConfigKeys(self) -> list[str]:
        ...

    @abstractmethod
    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...
