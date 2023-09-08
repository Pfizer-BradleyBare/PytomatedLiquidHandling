from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton.Backend import VantageBackend
from .Base import TransportDeviceABC, TransportOptions
from PytomatedLiquidHandling.HAL import DeckLocation


@dataclass
class VantageTrackGripper(TransportDeviceABC):
    BackendInstance: VantageBackend

    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...
