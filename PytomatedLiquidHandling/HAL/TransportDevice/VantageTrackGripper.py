from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton.Backend import VantageBackend
from PytomatedLiquidHandling.HAL import DeckLocation, LayoutItem

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

    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        ...

    def TransportTime(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ) -> float:
        return 0
