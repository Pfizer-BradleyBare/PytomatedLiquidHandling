from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton.Backend import VantageBackend
from PytomatedLiquidHandling.HAL import DeckLocation

from .Base import TransportDeviceABC


@dataclass
class VantageTrackGripper(TransportDeviceABC):
    BackendInstance: VantageBackend

    @dataclass
    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    @dataclass
    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    def Transport(self, TransportOptionsInstance: TransportDeviceABC.Options):
        ...

    def TransportTime(
        self, TransportOptionsInstance: TransportDeviceABC.Options
    ) -> float:
        return 0
