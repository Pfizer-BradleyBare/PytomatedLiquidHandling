from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from typing import Any

from plh.hal.tools import HALDevice


@dataclasses.dataclass
class HALError(Exception):
    """Base class for all HAL Errors."""

    error_device: HALDevice
    """The device that the error occurred on."""


@dataclasses.dataclass
class UserInteractionRequiredError(HALError, ABC):
    """Base class for all errors that require user intervention.
    This intervention is usually physical and not programmatic.
    """

    @abstractmethod
    def callback(
        self: UserInteractionRequiredError,
    ) -> None:
        """This function will perform cleanup or repeat action as necessary.
        NOTE: This callback may raise a new exception so beware of that.
        """
        ...


@dataclasses.dataclass
class UserInputRequiredError(HALError):
    """Base class for all user interaction errors that require an input to be provided by the user.
    This intervention is both physical and programmatic.
    """

    @abstractmethod
    def kwargs(self: UserInputRequiredError) -> dict[str, type]:
        """This returns a dictionary of the expected input key and it's type for the callback function.
        This is more for information purposes than anything else.
        """
        ...

    @abstractmethod
    def callback(
        self: UserInputRequiredError,
        **kwargs: dict[str, Any],
    ) -> None:
        """This function will perform cleanup or repeat action as necessary.
        kwargs can be used to figure out the input information required.
        NOTE: This callback may raise a new exception so beware of that.
        """
        ...
