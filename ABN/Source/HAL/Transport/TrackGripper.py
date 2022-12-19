from ..Layout import LayoutItem
from .BaseTransportDevice import (
    TransportableLabwareTracker,
    TransportDevice,
    TransportDevices,
)


class TrackGripper(TransportDevice):
    def __init__(
        self,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        TransportDevice.__init__(
            self,
            TransportDevices.InternalPlateGripper,
            TransportableLabwareTrackerInstance,
        )

    def Initialize(self):
        raise NotImplementedError

    def Deinitialize(self):
        raise NotImplementedError

    def MovePlate(
        self, SourceLayoutItem: LayoutItem, DestinationLayoutItem: LayoutItem
    ):
        raise NotImplementedError

    def GetConfigKeys(self) -> list[str]:
        return []
