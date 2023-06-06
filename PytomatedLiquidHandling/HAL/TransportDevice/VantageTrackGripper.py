from .BaseTransportDevice import (
    TransportDevice,
    TransportOptions,
)
from ...Driver.Hamilton.Backend import VantageBackend
from dataclasses import dataclass


@dataclass
class VantageTrackGripper(TransportDevice):
    BackendInstance: VantageBackend

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
