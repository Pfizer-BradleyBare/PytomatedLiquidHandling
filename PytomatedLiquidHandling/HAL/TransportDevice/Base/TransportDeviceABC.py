from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class PickupOptionsNotSupoortedError(BaseException):
    SourcePickupOptions: DeckLocation.Base.TransportConfig.Options
    DestinationPickupOptions: DeckLocation.Base.TransportConfig.Options


@dataclass
class WrongDeviceTransportOptionsError(BaseException):
    CurrentDevice: "TransportDeviceABC"
    TransportOptionsDevice: "TransportDeviceABC"


@dataclass
class TransportDevicesNotCompatibleError(BaseException):
    SourceTransportDevice: "TransportDeviceABC"
    DestinationTransportDevice: "TransportDeviceABC"


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

    def ValidateTransportOptions(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        UnsupportedLabware = list()

        if SourceLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            UnsupportedLabware.append(SourceLayoutItem.Labware)

        if DestinationLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            UnsupportedLabware.append(DestinationLayoutItem.Labware)

        if len(UnsupportedLabware) > 0:
            raise Labware.Base.LabwareNotSupportedError(UnsupportedLabware)

        SourceTransportDevice = (
            SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
        )
        DestinationTransportDevice = (
            DestinationLayoutItem.DeckLocation.TransportConfig.TransportDevice
        )
        if SourceTransportDevice != DestinationTransportDevice:
            raise TransportDevicesNotCompatibleError(
                SourceTransportDevice, DestinationTransportDevice
            )

        RequiredTransportDevice = SourceTransportDevice
        if type(self) != type(RequiredTransportDevice):
            raise WrongDeviceTransportOptionsError(self, RequiredTransportDevice)

        SourcePickupOptions = (
            SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions
        )
        DestinationPickupOptions = (
            DestinationLayoutItem.DeckLocation.TransportConfig.PickupOptions
        )
        if SourcePickupOptions != DestinationPickupOptions:
            raise PickupOptionsNotSupoortedError(
                SourcePickupOptions, DestinationPickupOptions
            )
        # We only care that the pickup options are compatible because that could determine plate orientation.
        # If orientation is incorrect then the plate dropoff will fail.

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
