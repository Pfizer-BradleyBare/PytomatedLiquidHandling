from ..Layout import LayoutItem
from .BaseTransportDevice import (
    TransportableLabwareTracker,
    TransportDevice,
    TransportDevices,
)


class COREGripper(TransportDevice):
    def __init__(
        self,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
        GripperSequence: str,
    ):
        self.GripperSequence: str = GripperSequence
        TransportDevice.__init__(
            self, TransportDevices.COREGripper, TransportableLabwareTrackerInstance
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
