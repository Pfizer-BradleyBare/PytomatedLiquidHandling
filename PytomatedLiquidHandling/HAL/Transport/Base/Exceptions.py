from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .TransportABC import TransportABC


@dataclass
class PickupOptionsNotEqualError(BaseException):
    """Trying to transport two LayoutItems that do not have equal PickupOptions.
    Equal PickupOptions are critical during transport because it ensures that the Labware
    will have the correct orientation during placement.

    Attributes:
    SourcePickupOptions: self explanatory
    DestinationPickupOptions: self explanatory
    """

    SourcePickupOptions: TransportABC.PickupOptions
    DestinationPickupOptions: TransportABC.PickupOptions


@dataclass
class WrongDeviceTransportOptionsError(BaseException):
    """Transport device is not the same as required by the DeckLocation TransportOptions.

    Attributes:
    CurrentDevice: Device on which you called Transport
    TransportOptionsDevice: Device required by the deck location
    """

    CurrentDevice: TransportABC
    TransportOptionsDevice: TransportABC


@dataclass
class TransportDevicesNotCompatibleError(BaseException):
    """Source and Destination DeckLocations require different TransportDevices

    Attributes:
    SourceTransportDevice: self explanatory
    DestinationTransportDevice: self explanatory
    """

    SourceTransportDevice: TransportABC
    DestinationTransportDevice: TransportABC
