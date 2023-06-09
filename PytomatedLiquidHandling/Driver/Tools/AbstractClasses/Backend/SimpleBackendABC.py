from dataclasses import dataclass, field
from typing import Type, TypeVar, cast

from .....Tools.AbstractClasses import UniqueObjectABC
from .....Tools.Logger import Logger
from ..Command import CommandABC
from .BackendABC import BackendABC

T = TypeVar("T", bound=CommandABC.Response)


@dataclass
class SimpleBackendABC(BackendABC):
    CurrentCommand: CommandABC | None = field(init=False, default=None)
    Response: CommandABC.Response | None = field(init=False, default=None)

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
            Response.SetProperty("State", True)
            Response.SetProperty("Details", "Respose available")

        else:
            Response.SetProperty("State", False)
            Response.SetProperty("Details", "Respose not available")

        return Response

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        BackendABC.WaitForResponseBlocking(self, CommandInstance)
        if self.CurrentCommand != CommandInstance:
            raise Exception(
                "You can only wait on a response for the currently executing command."
            )

        import time

        while self.GetStatus(CommandInstance).GetState() != True:
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

        if Response.GetState() == False:
            if Response.GetDetails() in CommandInstance.ExceptionABC.__Exceptions:
                raise CommandInstance.ExceptionABC.__Exceptions[Response.GetDetails()](
                    CommandInstance, Response
                )
            else:
                raise CommandInstance.UnhandledException(CommandInstance, Response)

        return cast(ResponseType, Response)
