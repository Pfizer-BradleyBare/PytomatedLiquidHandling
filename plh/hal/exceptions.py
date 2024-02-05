from __future__ import annotations

import dataclasses

from plh.hal.tools import HALDevice


@dataclasses.dataclass
class HALError(Exception):
    """Base class for all HAL Errors."""

    hal_devices: list[HALDevice]
    """Hal devices will provide error context. It is the responsibility of the exception catcher to
    parse the information to provide more context if required."""


@dataclasses.dataclass
class HardwareError(HALError):
    """Base class for all Hardware errors."""


@dataclasses.dataclass
class UserInteractionRequiredError(HALError):
    """Base class for all errors that require user intervention."""


@dataclasses.dataclass
class UserInputRequiredError(UserInteractionRequiredError):
    """Base class for all user interaction errors that require an input to be provided by the user."""
