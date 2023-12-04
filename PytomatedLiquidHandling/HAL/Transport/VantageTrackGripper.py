from dataclasses import field

from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TransportABC


class VantageTrackGripper(TransportABC):
    Backend: Backend.VantageTrackGripperEntryExit

    @dataclass
    class PickupOptions(TransportABC.PickupOptions):
        ...

    @dataclass
    class DropoffOptions(TransportABC.DropoffOptions):
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
