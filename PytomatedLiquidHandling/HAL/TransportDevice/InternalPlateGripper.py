from ..LayoutItem.BaseLayoutItem import LayoutItem
from .BaseTransportDevice import TransportableLabwareTracker, TransportDevice


class InternalPlateGripper(TransportDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        CustomErrorHandling: bool,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        TransportDevice.__init__(
            self,
            UniqueIdentifier,
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

    def Transport(
        self,
        SourceLayoutItem: LayoutItem,
        DestinationLayoutItem: LayoutItem,
    ):
        ...

    def GetConfigKeys(self) -> list[str]:
        return []
