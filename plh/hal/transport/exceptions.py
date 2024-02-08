from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from plh.hal import layout_item
from plh.hal.exceptions import HALError, UserInteractionRequiredError

from .options import GetPlaceOptions

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

    layout_item: layout_item.LayoutItemBase
    """layout_item that failed to be picked up"""

    def callback(self: GetHardwareError) -> None:
        """No repeat or cleanup actions are required"""
        ...


@dataclass
class PlaceHardwareError(TransportHardwareError):
    """A hardware error that could occur when placing up a layout item.
    An example could be a missing layout item like a lid.
    The gripper thinks it has a lid but when it places the lid the gripper may be tighter than the plate width.
    """

    layout_item: layout_item.LayoutItemBase
    """layout_item that failed to be placed"""

    def callback(self: PlaceHardwareError) -> None:
        """Retries the place operation. We cannot leave a plate picked up.
        NOTE: Due to the nature of the error. The source and destination are now the same.
        """
        self.error_device.place(
            GetPlaceOptions(
                source_layout_item=self.layout_item,
                destination_layout_item=self.layout_item,
            ),
        )
