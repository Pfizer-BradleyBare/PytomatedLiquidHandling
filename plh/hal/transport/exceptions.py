from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from plh.hal.exceptions import HALError, UserInteractionRequiredError

if TYPE_CHECKING:
    from .transport_base import TransportBase


@dataclass
class WrongTransportDeviceError(HALError):
    """Transport device is not the same as required by the DeckLocation TransportOptions."""

    error_device: TransportBase

    ViableTransportDevices: list[TransportBase]

    def __str__(self) -> str:
        return f"{self.error_device.identifier} != [{', '.join([device.identifier for device in self.ViableTransportDevices])}]"


@dataclass
class TransportHardwareError(UserInteractionRequiredError):
    """Base class for hardware errors that occur while using transport devices."""

    error_device: TransportBase


@dataclass
class GetHardwareError(TransportHardwareError):
    """A hardware error that could occur when picking up a layout item.
    An example could be incorrect grip height which causes the grippers to hit the plate.
    """


@dataclass
class PlaceHardwareError(TransportHardwareError):
    """A hardware error that could occur when placing up a layout item.
    An example could be a missing layout item like a lid.
    The gripper thinks it has a lid but when it places the lid the gripper may be tighter than the plate width.
    """
