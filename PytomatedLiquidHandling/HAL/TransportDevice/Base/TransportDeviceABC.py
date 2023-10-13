from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class PickupOptionsNotEqualError(BaseException):
    """Trying to transport two LayoutItems that do not have equal PickupOptions.
    Equal PickupOptions are critical during transport because it ensures that the Labware
    will have the correct orientation during placement.

    Attributes:
    SourcePickupOptions: self explanatory
    DestinationPickupOptions: self explanatory
    """

    SourcePickupOptions: DeckLocation.Base.TransportConfig.Options
    DestinationPickupOptions: DeckLocation.Base.TransportConfig.Options


@dataclass
class WrongDeviceTransportOptionsError(BaseException):
    """Transport device is not the same as required by the DeckLocation TransportOptions.

    Attributes:
    CurrentDevice: Device on which you called Transport
    TransportOptionsDevice: Device required by the deck location
    """

    CurrentDevice: "TransportDeviceABC"
    TransportOptionsDevice: "TransportDeviceABC"


@dataclass
class TransportDevicesNotCompatibleError(BaseException):
    """Source and Destination DeckLocations require different TransportDevices

    Attributes:
    SourceTransportDevice: self explanatory
    DestinationTransportDevice: self explanatory
    """

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
        if SourceLayoutItem.Labware != DestinationLayoutItem.Labware:
            raise Labware.Base.LabwareNotEqualError(
                SourceLayoutItem.Labware, DestinationLayoutItem.Labware
            )
        # Are the labware compatible?

        UnsupportedLabware = list()

        if SourceLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            UnsupportedLabware.append(SourceLayoutItem.Labware)

        if DestinationLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            UnsupportedLabware.append(DestinationLayoutItem.Labware)

        if len(UnsupportedLabware) > 0:
            raise Labware.Base.LabwareNotSupportedError(UnsupportedLabware)
        # Are both source and destination labware supported by this device?

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
        # Are the source and destination accessible by the same transport device?

        RequiredTransportDevice = SourceTransportDevice
        if type(self) != type(RequiredTransportDevice):
            raise WrongDeviceTransportOptionsError(self, RequiredTransportDevice)
        # Is this device actually needed by this layout item?

        SourcePickupOptions = (
            SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions
        )
        DestinationPickupOptions = (
            DestinationLayoutItem.DeckLocation.TransportConfig.PickupOptions
        )
        if SourcePickupOptions != DestinationPickupOptions:
            raise PickupOptionsNotEqualError(
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
