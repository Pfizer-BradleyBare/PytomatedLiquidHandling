from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Callable

from plh.hal.tools import HALDevice


@dataclasses.dataclass
class HALError(Exception):
    """Base class for all HAL Errors."""

    error_device: HALDevice
    """The device that the error occurred on."""

    associated_devices: list[HALDevice]
    """Other devices that were assoicated with the error. These will provide extra error context.
    It is the responsibility of the exception catcher to parse the information to provide more context if they wish."""


@dataclasses.dataclass
class UserInteractionRequiredError(HALError, ABC):
    """Base class for all errors that require user intervention.
    This intervention is usually physical and not programmatic.
    """

    @abstractmethod
    def perform_error_handling(
        self: UserInteractionRequiredError,
        dialog_function: Callable[..., None],
    ) -> None:
        """This function should call the user supplied dialog_function then perform cleanup or repeat action as necessary.
        NOTE: The user supplied function in this context should NOT return a value.
        """
        ...


@dataclasses.dataclass
class UserInputRequiredError(HALError):
    """Base class for all user interaction errors that require an input to be provided by the user.
    This intervention is both physical and programmatic.
    """

    @abstractmethod
    def perform_error_handling(
        self: UserInputRequiredError,
        dialog_function: Callable[..., Any],
    ) -> None:
        """This function should call the user supplied dialog_function then perform cleanup or repeat action as necessary.
        NOTE: The user supplied function in this context MUST return a value.
        """
        ...
