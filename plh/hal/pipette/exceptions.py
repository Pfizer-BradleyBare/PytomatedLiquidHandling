from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from plh.hal.exceptions import HALError, UserInteractionRequiredError

if TYPE_CHECKING:
    from .pipette_base import PipetteBase


@dataclass
class LiquidClassCategoryNotSupportedError(Exception):
    """HAL device does not support your Labware. This can be thrown for any LayoutItem inputs.

    Attributes
    ----------
    Categories: List of category names and associated volumes tuple[Name,Volume] that were not supported
    """

    Categories: list[str]


@dataclass
class TransferHardwareError(UserInteractionRequiredError):
    """Base class for hardware errors that occur during a transfer step.
    NOTE: All hardware errors that occur during a transfer will be ejected then the operation should be repeated.
    """

    error_device: PipetteBase
    _channel_numbers_to_waste: list[int]

    def perform_error_handling(
        self: TransferHardwareError,
        dialog_function: Callable[[HALError], None],
    ) -> None:
        """All transfer hardware errors must be handled by ejecting the current tips to waste. So this function should do that."""
        current_exception = self

        while True:
            dialog_function(current_exception)

            try:
                self.error_device._waste(self._channel_numbers_to_waste)
                break
                # Try to call the waste method, if it is successful then howdy doody. If not, then retry the dialog with our new error.
            except TransferHardwareError as e:
                current_exception = e


@dataclass
class PickupHardwareError(TransferHardwareError):
    """A hardware error that could occur during a tip pickup step.
    An example could be the wrong teir height select for stacked tips. If it is incorrect the channels could crash into the teirs during pickup.
    """


@dataclass
class AspirateHardwareError(TransferHardwareError):
    """A hardware error that could occur during a aspiration step.
    An example could be that a closeable container was not opened correctly, thus the tips crashed into the lid and bent.
    """


@dataclass
class DispenseHardwareError(TransferHardwareError):
    """A hardware error that could occur during a dispense step.
    Similar to ```AspirateHardwareError```, an example could be that a closeable container was not opened correctly, thus the tips crashed into the lid and bent.
    """


@dataclass
class EjectHardwareError(TransferHardwareError):
    """A hardware error that could occur during an eject step.
    An example could be that the waste area is overflowing and the channel hit some waste during the eject cycle.
    """
