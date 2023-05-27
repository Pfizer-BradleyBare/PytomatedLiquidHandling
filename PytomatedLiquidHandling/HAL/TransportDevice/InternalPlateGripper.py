from ..LayoutItem.BaseLayoutItem import LayoutItem
from .BaseTransportDevice import TransportableLabwareTracker, TransportDevice
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class InternalPlateGripper(TransportDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
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

    def Transport(
        self,
        SourceLayoutItem: LayoutItem,
        DestinationLayoutItem: LayoutItem,
    ):
        ...

    def GetConfigKeys(self) -> list[str]:
        return []
