from abc import abstractmethod

from .....Tools.AbstractClasses import UniqueObjectABC
from ..Command import CommandABC


class BackendABC(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.CurrentCommand: CommandABC | None = None
        self.Response: CommandABC.Response | None = None

    @staticmethod
    def Decorator_ExecuteCommand(DecoratedFunction):
        def inner(*args, **kwargs):
            self = args[0]
            if not isinstance(self, BackendABC):
                raise Exception("You used this decorator incorrectly...")

            if self.CurrentCommand is not None:
                raise Exception(
                    "Command is already being executed. Wait on command to compelete..."
                )

            return DecoratedFunction(*args, **kwargs)

        return inner

    @abstractmethod
    def StartBackend(self):
        ...

    @abstractmethod
    def StopBackend(self):
        ...

    @abstractmethod
    def ExecuteCommand(self, CommandInstance: CommandABC):
        ...

    @abstractmethod
    def GetStatus(self) -> CommandABC.Response:
        ...

    def GetResponse(self) -> CommandABC.Response:
        if self.CurrentCommand is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.Response is None:
            raise Exception("Response not available. Check status first...")

        Response = self.Response

        self.CurrentCommand = None
        self.Response = None

        return Response
