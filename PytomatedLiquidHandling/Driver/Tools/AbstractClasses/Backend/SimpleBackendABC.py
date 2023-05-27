import time
from abc import abstractmethod
from typing import Type, TypeVar, cast

from .BackendABC import BackendABC
from .....Tools.AbstractClasses import UniqueObjectABC
from .....Tools.Logger import Logger
from ..Command import CommandABC

T = TypeVar("T", bound=CommandABC.Response)


class SimpleBackendABC(BackendABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger):
        BackendABC.__init__(self, UniqueIdentifier, LoggerInstance)
        self.CurrentCommand: CommandABC | None = None
        self.Response: CommandABC.Response | None = None

    def ExecuteCommand(self, CommandInstance: CommandABC):
        BackendABC.ExecuteCommand(self, CommandInstance)
        if self.CurrentCommand is not None:
            raise Exception(
                "Command is already being executed. Wait on command to compelete..."
            )

        self.CurrentCommand = CommandInstance

    def GetStatus(self, CommandInstance: CommandABC) -> CommandABC.Response:
        BackendABC.GetStatus(self, CommandInstance)
        if self.CurrentCommand is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CurrentCommand != CommandInstance:
            raise Exception(
                "You can only get a status for the currently executing command."
            )

        Response = CommandABC.Response({})

        if not self.Response is None:
            Response.SetProperty("StatusCode", 0)
            Response.SetProperty("Details", "Respose available")

        else:
            Response.SetProperty("StatusCode", -1)
            Response.SetProperty("Details", "Respose not available")

        return Response

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        BackendABC.WaitForResponseBlocking(self, CommandInstance)
        if self.CurrentCommand != CommandInstance:
            raise Exception(
                "You can only wait on a response for the currently executing command."
            )

        while self.GetStatus(CommandInstance).GetStatusCode() != 0:
            ...

    def GetResponse(self, CommandInstance: CommandABC, ResponseType: Type[T]) -> T:
        BackendABC.GetResponse(self, CommandInstance, ResponseType)
        if self.CurrentCommand is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CurrentCommand != CommandInstance:
            raise Exception(
                "You can only get a response for the currently executing command."
            )

        if self.Response is None:
            raise Exception("Response not available. Check status first...")

        Response = self.Response

        self.CurrentCommand = None
        self.Response = None

        return cast(ResponseType, Response)
