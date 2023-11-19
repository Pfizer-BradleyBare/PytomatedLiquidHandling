from typing import Type, TypeVar, cast

from pydantic import PrivateAttr, ValidationError

from ..Command import CommandABC
from ..Response import ResponseABC
from .BackendABC import BackendABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


class CommandStatusResponse(ResponseABC):
    ResponseReady: bool


class SimpleBackendABC(BackendABC):
    _Command: CommandABC | None = PrivateAttr(default=None)
    _Response: dict | None = PrivateAttr(default=None)
    _Exception: Exception | None = PrivateAttr(default=None)

    def ExecuteCommand(self, CommandInstance: CommandABC):
        BackendABC.ExecuteCommand(self, CommandInstance)
        if self._Command is not None:
            raise Exception(
                "Command is already being executed. Wait on command to compelete..."
            )

        self._Command = CommandInstance

    def GetCommandStatus(self, CommandInstance: CommandABC) -> CommandStatusResponse:
        BackendABC.GetCommandStatus(self, CommandInstance)
        if self._Command is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self._Command != CommandInstance:
            raise Exception(
                "You can only get a status for the currently executing command."
            )

        if not self._Response is None:
            return CommandStatusResponse(ResponseReady=True)

        else:
            return CommandStatusResponse(ResponseReady=False)

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        BackendABC.WaitForResponseBlocking(self, CommandInstance)
        if self._Command != CommandInstance:
            raise Exception(
                "You can only wait on a response for the currently executing command."
            )

        while self.GetCommandStatus(CommandInstance).ResponseReady != True:
            ...

    def GetResponse(
        self, CommandInstance: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
        BackendABC.GetResponse(self, CommandInstance, ResponseType)

        if self._Command is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self._Command != CommandInstance:
            raise Exception(
                "You can only get a response for the currently executing command."
            )

        if self._Response is None:
            raise Exception("Response not available. Check status first...")

        Response = self._Response

        self._Command = None
        self._Response = None

        if self._Exception is not None:
            Exception = self._Exception
            self._Exception = None
            raise Exception
        # TODO!!!

        return ResponseType(**Response)
