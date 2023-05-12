from abc import abstractmethod

from .....Tools.AbstractClasses import UniqueObjectABC
from ...AbstractClasses import CommandABC


class BackendABC(UniqueObjectABC):
    @abstractmethod
    def StartBackend(self):
        ...

    @abstractmethod
    def StopBackend(self):
        ...

    @abstractmethod
    def GetRawStatus(self) -> int:
        ...

    @abstractmethod
    def ExecuteCommand(self, CommandInstance: CommandABC):
        ...

    @abstractmethod
    def GetStatus(self) -> CommandABC.Response:
        ...

    @abstractmethod
    def GetResponse(self) -> CommandABC.Response:
        ...
