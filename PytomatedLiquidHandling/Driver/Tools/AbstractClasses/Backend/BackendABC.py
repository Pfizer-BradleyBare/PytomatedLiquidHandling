from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Type, TypeVar

from .....Tools.AbstractClasses import UniqueObjectABC
from .....Tools.Logger import Logger
from ..Command import CommandABC

T = TypeVar("T", bound=CommandABC.Response)


@dataclass
class BackendABC(UniqueObjectABC):
    LoggerInstance: Logger
    IsRunning: bool = field(init=False, default=False)

    def __CheckRunning(self):
        if self.IsRunning == False:
            raise Exception("You must start the backend before interacting")

    @abstractmethod
    def StartBackend(self):
        self.IsRunning = True

    @abstractmethod
    def StopBackend(self):
        self.IsRunning = False

    @abstractmethod
    def ExecuteCommand(self, CommandInstance: CommandABC):
        self.__CheckRunning()

    @abstractmethod
    def GetCommandStatus(self, CommandInstance: CommandABC) -> CommandABC.Response:
        self.__CheckRunning()

    @abstractmethod
    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        self.__CheckRunning()

    @abstractmethod
    def GetResponse(self, CommandInstance: CommandABC, ResponseType: Type[T]) -> T:
        self.__CheckRunning()
