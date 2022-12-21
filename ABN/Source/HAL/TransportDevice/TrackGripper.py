from ...Driver.Tools import CommandTracker
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

    def Initialize(self) -> CommandTracker:
        ...

    def Deinitialize(self) -> CommandTracker:
        ...

    def Transport(
        self, SourceLayoutItem: LayoutItem, DestinationLayoutItem: LayoutItem
    ) -> CommandTracker:
        ...

    def GetConfigKeys(self) -> list[str]:
        return []
