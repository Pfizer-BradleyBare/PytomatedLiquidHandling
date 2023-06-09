from dataclasses import dataclass, field
from typing import Type, TypeVar, cast

from ..Command import CommandABC
from .BackendABC import BackendABC

T = TypeVar("T", bound=CommandABC.Response)


@dataclass
class SimpleBackendABC(BackendABC):
    CommandInstance: CommandABC | None = field(init=False, default=None)
    ResponseInstance: CommandABC.Response | None = field(init=False, default=None)

    def ExecuteCommand(self, CommandInstance: CommandABC):
        BackendABC.ExecuteCommand(self, CommandInstance)
        if self.CommandInstance is not None:
            raise Exception(
                "Command is already being executed. Wait on command to compelete..."
            )

        self.CommandInstance = CommandInstance

    def GetCommandStatus(self, CommandInstance: CommandABC) -> CommandABC.Response:
        BackendABC.GetCommandStatus(self, CommandInstance)
        if self.CommandInstance is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CommandInstance != CommandInstance:
            raise Exception(
                "You can only get a status for the currently executing command."
            )

        Response = CommandABC.Response({})

        if not self.ResponseInstance is None:
            Response.SetProperty("State", True)
            Response.SetProperty("Details", "Respose available")

        else:
            Response.SetProperty("State", False)
            Response.SetProperty("Details", "Respose not available")

        return Response

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        BackendABC.WaitForResponseBlocking(self, CommandInstance)
        if self.CommandInstance != CommandInstance:
            raise Exception(
                "You can only wait on a response for the currently executing command."
            )

        while self.GetCommandStatus(CommandInstance).GetState() != True:
            ...

    @staticmethod
    def CheckExceptions(
        CommandInstance: CommandABC, ResponseInstance: CommandABC.Response
    ):
        if ResponseInstance.GetState() == False:
            if (
                ResponseInstance.GetDetails()
                in CommandInstance.ExceptionABC.__Exceptions
            ):
                raise CommandInstance.ExceptionABC.__Exceptions[
                    ResponseInstance.GetDetails()
                ](CommandInstance, ResponseInstance)
            else:
                raise CommandInstance.UnhandledException(
                    CommandInstance, ResponseInstance
                )

    def GetResponse(self, CommandInstance: CommandABC, ResponseType: Type[T]) -> T:
        BackendABC.GetResponse(self, CommandInstance, ResponseType)
        if self.CommandInstance is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CommandInstance != CommandInstance:
            raise Exception(
                "You can only get a response for the currently executing command."
            )

        if self.ResponseInstance is None:
            raise Exception("Response not available. Check status first...")

        Response = self.ResponseInstance

        self.CommandInstance = None
        self.ResponseInstance = None

        SimpleBackendABC.CheckExceptions(CommandInstance, Response)

        return cast(ResponseType, Response)
