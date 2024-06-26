from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from plh.implementation.exceptions import HALError, UserInteractionRequiredError

from .options import AspirateOptions, DispenseOptions

if TYPE_CHECKING:
    from .pipette_base import PipetteBase


@dataclass
class LiquidClassCategoryNotSupportedError(HALError):
    """HAL device does not support your Labware. This can be thrown for any LayoutItem inputs."""

    error_device: PipetteBase

    category: str

    volume: float


@dataclass
class IncompleteTransferError(HALError):
    """You're transfer operation experienced an error. You should retry with the following options."""

    options: tuple[AspirateOptions, *tuple[DispenseOptions, ...]]


@dataclass
class PipetteHardwareError(UserInteractionRequiredError):
    """Base class for hardware errors that occur while using pipette devices.
    NOTE: All hardware errors that occur during a transfer will be ejected then the operation should be repeated.
    """

    error_device: PipetteBase

    _options: list[tuple[int, tuple[str, str]]]

    def callback(
        self: PipetteHardwareError,
    ) -> None:
        """All transfer hardware errors must be handled by ejecting the current tips to waste. So this function does that."""
        self.error_device._eject(*self._options)


@dataclass
class PickupHardwareError(PipetteHardwareError):
    """A hardware error that could occur during a tip pickup step.
    An example could be the wrong teir height select for stacked tips. If it is incorrect the channels could crash into the teirs during pickup.
    """


@dataclass
class AspirateHardwareError(PipetteHardwareError):
    """A hardware error that could occur during a aspiration step.
    An example could be that a closeable container was not opened correctly, thus the tips crashed into the lid and bent.
    """


@dataclass
class DispenseHardwareError(PipetteHardwareError):
    """A hardware error that could occur during a dispense step.
    Similar to ```AspirateHardwareError```, an example could be that a closeable container was not opened correctly, thus the tips crashed into the lid and bent.
    """


@dataclass
class EjectHardwareError(PipetteHardwareError):
    """A hardware error that could occur during an eject step.
    An example could be that the waste area is overflowing and the channel hit some waste during the eject cycle.
    """
