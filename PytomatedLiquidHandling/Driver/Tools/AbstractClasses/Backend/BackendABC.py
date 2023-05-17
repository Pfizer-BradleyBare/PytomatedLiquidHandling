from abc import abstractmethod

from .....Tools.AbstractClasses import UniqueObjectABC
from .....Tools.Logger import Logger
from ..Command import CommandABC


class BackendABC(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.LoggerInstance: Logger = LoggerInstance
        self.CurrentCommand: CommandABC | None = None
        self.Response: CommandABC.Response | None = None

    @abstractmethod
    def StartBackend(self):
        ...

    @abstractmethod
    def StopBackend(self):
        ...

    def ExecuteCommand(self, CommandInstance: CommandABC):
        if self.CurrentCommand is not None:
            raise Exception(
                "Command is already being executed. Wait on command to compelete..."
            )

        self.CurrentCommand = CommandInstance

    def GetStatus(self, CommandInstance: CommandABC) -> CommandABC.Response:
        if self.CurrentCommand is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CurrentCommand == CommandInstance:
            raise Exception(
                "You can only get a response for the currently executing command."
            )

        Response = CommandABC.Response({})

        if self.Response is None:
            Response.SetProperty("StatusCode", 0)
            Response.SetProperty("Details", "Respose available")

        else:
            Response.SetProperty("StatusCode", -1)
            Response.SetProperty("Details", "Respose not available")

        return Response

    def GetResponse(self, CommandInstance: CommandABC) -> CommandABC.Response:
        if self.CurrentCommand is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CurrentCommand == CommandInstance:
            raise Exception(
                "You can only get a response for the currently executing command."
            )

        if self.Response is None:
            raise Exception("Response not available. Check status first...")

        Response = self.Response

        self.CurrentCommand = None
        self.Response = None

        return Response
