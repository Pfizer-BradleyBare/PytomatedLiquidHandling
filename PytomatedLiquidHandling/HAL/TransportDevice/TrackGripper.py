from .BaseTransportDevice import (
    TransportableLabwareTracker,
    TransportDevice,
    TransportOptions,
)
from ...Driver.Hamilton.Backend import VantageBackend


class TrackGripper(TransportDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: VantageBackend,
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

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...

    def GetGetConfigKeys(self) -> list[str]:
        ...

    def GetPlaceConfigKeys(self) -> list[str]:
        ...
