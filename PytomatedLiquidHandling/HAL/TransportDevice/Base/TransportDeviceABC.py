from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class TransportDeviceABC(InterfaceABC, HALObject):
    SupportedLabwares: list[Labware.Base.LabwareABC]
    _LastTransportFlag: bool = field(init=False, default=True)

    @dataclass
    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    @dataclass
    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    def IsTransportSupported(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ) -> bool:
        if SourceLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            return False

        if DestinationLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            return False

        if (
            SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions
            != DestinationLayoutItem.DeckLocation.TransportConfig.PickupOptions
        ):
            return False
        # We only care that the pickup options are compatible because that could determine plate orientation.
        # If orientation is incorrect then the plate dropoff will fail.

        return True

    @abstractmethod
    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        ...

    @abstractmethod
    def TransportTime(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ) -> float:
        ...
