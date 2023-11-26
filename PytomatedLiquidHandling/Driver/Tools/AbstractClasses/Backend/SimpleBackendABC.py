from typing import Type, TypeVar, cast

from pydantic import PrivateAttr, ValidationError

from ..Command import CommandABC
from ..Response import ResponseABC
from .BackendABC import BackendABC, CommandStatusResponse

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


class SimpleBackendABC(BackendABC):
    _Command: CommandABC | None = PrivateAttr(default=None)
    _Response: dict | Exception | None = PrivateAttr(default=None)

    def ExecuteCommand(self, Command: CommandABC):
        BackendABC.ExecuteCommand(self, Command)
        if self._Command is not None:
            raise RuntimeError(
                "Command is already being executed. Wait on command to compelete..."
            )

        self._Command = Command

    def GetCommandStatus(self, Command: CommandABC) -> CommandStatusResponse:
        BackendABC.GetCommandStatus(self, Command)
        if self._Command is None:
            raise RuntimeError(
                "No Command currently executing. Execute a command first..."
            )

        if self._Command != Command:
            raise RuntimeError(
                "You can only get a status for the currently executing command."
            )

        if not self._Response is None:
            return CommandStatusResponse(ResponseReady=True)

        else:
            return CommandStatusResponse(ResponseReady=False)

    def WaitForResponseBlocking(self, Command: CommandABC):
        BackendABC.WaitForResponseBlocking(self, Command)

        while self.GetCommandStatus(Command).ResponseReady != True:
            ...

    def GetResponse(
        self, Command: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
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
            raise RuntimeError("Response not available. Check status first...")

        Response = self._Response

        self._Command = None
        self._Response = None

        if isinstance(Response, Exception):
            raise Response

        return ResponseType(**Response)
