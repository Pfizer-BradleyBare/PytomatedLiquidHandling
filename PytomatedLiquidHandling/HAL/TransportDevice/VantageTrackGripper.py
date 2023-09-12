from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton.Backend import VantageBackend
from PytomatedLiquidHandling.HAL import DeckLocation

from .Base import TransportDeviceABC, TransportOptions


@dataclass
class VantageTrackGripper(TransportDeviceABC):
    BackendInstance: VantageBackend

    @dataclass
    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    @dataclass
    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...
