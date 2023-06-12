from dataclasses import dataclass, field
from typing import Type, TypeVar, cast

from ..Command import CommandABC
from ..Response import ResponseABC
from .BackendABC import BackendABC
from ..Exception import UnhandledException

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclass
class SimpleBackendABC(BackendABC):
    CommandInstance: CommandABC | None = field(init=False, default=None)
    ResponseInstance: ResponseABC | None = field(init=False, default=None)

    def ExecuteCommand(self, CommandInstance: CommandABC):
        BackendABC.ExecuteCommand(self, CommandInstance)
        if self.CommandInstance is not None:
            raise Exception(
                "Command is already being executed. Wait on command to compelete..."
            )

        self.CommandInstance = CommandInstance

    def GetCommandStatus(self, CommandInstance: CommandABC) -> ResponseABC:
        BackendABC.GetCommandStatus(self, CommandInstance)
        if self.CommandInstance is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CommandInstance != CommandInstance:
            raise Exception(
                "You can only get a status for the currently executing command."
            )

        Response = ResponseABC({})

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

    def CheckExceptions(
        self, CommandInstance: CommandABC, ResponseInstance: ResponseABC
    ):
        if ResponseInstance.GetState() == False:
            for Exception in self.Exceptions:
                if Exception.ErrorCode in ResponseInstance.GetDetails():
                    raise Exception(CommandInstance, ResponseInstance)

            raise UnhandledException(CommandInstance, ResponseInstance)

    def GetResponse(
        self, CommandInstance: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
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

        self.CheckExceptions(CommandInstance, Response)

        return cast(ResponseType, Response)
