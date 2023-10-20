from dataclasses import field
from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TransportDeviceABC


class VantageTrackGripper(TransportDeviceABC):
    @dataclass
    class PickupOptions(TransportDeviceABC.PickupOptions):
        ...

    @dataclass
    class DropoffOptions(TransportDeviceABC.DropoffOptions):
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
