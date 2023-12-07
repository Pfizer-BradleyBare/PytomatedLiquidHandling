from typing import Type, TypeVar, cast

from pydantic import PrivateAttr, ValidationError

from ..Command import CommandABC
from ..Response import ResponseABC
from .BackendABC import BackendABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


class SimpleBackendABC(BackendABC):
    """The simplest implementation of a backend. This class will support 99% of backends."""

    _Command: CommandABC | None = PrivateAttr(default=None)
    """The currently executing command. If ```None``` then no command is currently executing."""

    _Response: dict | Exception | None = PrivateAttr(default=None)
    """The information for the command. If ```None``` then the command execution has not completed."""

    def ExecuteCommand(self, Command: CommandABC):
        """Only one command may be executed at a time.
        You must ```WaitForResponseBlocking(Command)``` and ```GetResponse(Command,ResponseType)``` before executing another command.
        """
        BackendABC.ExecuteCommand(self, Command)
        if self._Command is not None:
            raise RuntimeError(
                "Command is already being executed. Wait on command to compelete..."
            )

        self._Command = Command

    def WaitForResponseBlocking(self, Command: CommandABC):
        """Waits for execution of ```Command``` to complete.

        If the ```Command``` does not match the executing command or no command is executing then ```RuntimeError``` is raised.
        """
        BackendABC.WaitForResponseBlocking(self, Command)

        if self._Command is None:
            raise RuntimeError(
                "No Command currently executing. Execute a command first..."
            )

        if self._Command != Command:
            raise RuntimeError("You can only wait on the currently executing command.")

        while self._Response is None:
            ...

    def GetResponse(
        self, Command: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
        """Returns a response described by ```ResponseType``` for the executed ```Command```.

        If the ```Command``` does not match the executing command, no command is executing, or a command execution is not complete then ```RuntimeError``` is raised.
        """
        BackendABC.GetResponse(self, Command, ResponseType)

        if self._Command is None:
            raise RuntimeError(
                "No Command currently executing. Execute a command first..."
            )

        if self._Command != Command:
            raise RuntimeError(
                "You can only get a response for the currently executing command."
            )

        if self._Response is None:
            raise RuntimeError(
                "Response not available. Call WaitForResponseBlocking first..."
            )

        Response = self._Response

        self._Command = None
        self._Response = None

        if isinstance(Response, Exception):
            raise Response

        return ResponseType(**Response)
