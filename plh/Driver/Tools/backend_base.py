from __future__ import annotations

from abc import abstractmethod
from dataclasses import field
from typing import TYPE_CHECKING, TypeVar

from pydantic import dataclasses

from .response_base import ResponseBase

if TYPE_CHECKING:
    from .command_base import CommandBase

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseBase)


@dataclasses.dataclass(kw_only=True)
class BackendBase:
    """A base class for all backends."""

    identifier: str
    """A name given to the backend. Creates compatibility with the HAL layer."""

    is_running: bool = field(init=False, default=False)
    """Is the backend running?"""

    @abstractmethod
    def start(self: BackendBase) -> None:
        """Should start the system software then establish communication. You should only call the method once."""
        if self.is_running is True:
            msg = f"{type(self).__name__} backend is already running"
            raise RuntimeError(msg)
        self.is_running = True

    @abstractmethod
    def stop(self: BackendBase) -> None:
        """Should close the communication layer then kill the system software."""
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)
        self.is_running = False

    @abstractmethod
    def execute(self: BackendBase, command: CommandBase) -> None:
        """Delivers the ```Command``` to the system to be executed."""
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)

    @abstractmethod
    def wait(self: BackendBase, command: CommandBase) -> None:
        """Waits for execution of ```Command``` to complete."""
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)

    @abstractmethod
    def acknowledge(
        self: BackendBase,
        command: CommandBase,
        response_type: type[ResponseABCType],
    ) -> ResponseABCType:
        """Returns a response described by ```ResponseType``` for the executed ```Command```.
        Response data is parsed by pydantic into the type specified. You may discard the response.
        NOTE: Exceptions may be raised upon execution. See the specific backend for exception details.
        """
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)
