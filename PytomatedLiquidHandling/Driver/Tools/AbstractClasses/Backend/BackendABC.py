from abc import abstractmethod

from .....Tools.AbstractClasses import UniqueObjectABC
from .....Tools.Logger import Logger
from ..Command import CommandABC


class BackendABC(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.LoggerInstance: Logger = LoggerInstance

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

    @abstractmethod
    def GetResponse(self, CommandInstance: CommandABC) -> CommandABC.Response:
        ...
