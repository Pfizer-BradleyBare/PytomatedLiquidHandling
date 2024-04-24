from __future__ import annotations

from dataclasses import field
from typing import TypeVar

from pydantic import dataclasses

from .backend_base import BackendBase
from .command_base import CommandBase
from .response_base import ResponseBase

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseBase)


class Config:
    arbitrary_types_allowed = True


@dataclasses.dataclass(kw_only=True, config=Config)
class BackendSimpleBase(BackendBase):
    """The simplest implementation of a backend. This class will support 99% of backends."""

    _command: CommandBase | None = field(init=False, default=None)
    """The currently executing command. If ```None``` then no command is currently executing."""

    _response: dict | Exception | None = field(init=False, default=None)
    """The information for the command. If ```None``` then the command execution has not completed."""

    def execute(self: BackendSimpleBase, command: CommandBase) -> None:
        """Only one command may be executed at a time.
        You must ```WaitForResponseBlocking(Command)``` and ```GetResponse(Command,ResponseType)``` before executing another command.
        """
        BackendBase.execute(self, command)
        if self._command is not None:
            msg = "Command is already being executed. Wait on command to compelete..."
            raise RuntimeError(msg)

        self._command = command

    def wait(self: BackendSimpleBase, command: CommandBase) -> None:
        """Waits for execution of ```Command``` to complete.

        If the ```Command``` does not match the executing command or no command is executing then ```RuntimeError``` is raised.
        """
        BackendBase.wait(self, command)

        if self._command is None:
            msg = "No Command currently executing. Execute a command first..."
            raise RuntimeError(msg)

        if self._command != command:
            msg = "You can only wait on the currently executing command."
            raise RuntimeError(msg)

        while self._response is None:
            ...

    def acknowledge(
        self: BackendSimpleBase,
        command: CommandBase,
        response_type: type[ResponseABCType],
    ) -> ResponseABCType:
        """Returns a response described by ```ResponseType``` for the executed ```Command```.

        If the ```Command``` does not match the executing command, no command is executing, or a command execution is not complete then ```RuntimeError``` is raised.
        """
        BackendBase.acknowledge(self, command, response_type)

        if self._command is None:
            msg = "No Command currently executing. Execute a command first..."
            raise RuntimeError(msg)

        if self._command != command:
            msg = "You can only get a response for the currently executing command."
            raise RuntimeError(msg)

        if self._response is None:
            msg = "Response not available. Call WaitForResponseBlocking first..."
            raise RuntimeError(msg)

        response = self._response

        self._command = None
        self._response = None

        if isinstance(response, Exception):
            raise response

        return response_type(**response)
