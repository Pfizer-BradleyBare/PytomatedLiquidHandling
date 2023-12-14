from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .TransportABC import TransportABC


@dataclass
class WrongTransportDeviceError(BaseException):
    """Transport device is not the same as required by the DeckLocation TransportOptions.

    Attributes:
    CurrentDevice: Device on which you called Transport
    TransportOptionsDevice: Device required by the deck location
    """

    CurrentDevice: TransportABC
    ViableTransportDevices: list[TransportABC]
