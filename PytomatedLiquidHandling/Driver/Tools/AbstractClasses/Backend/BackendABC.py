import time
from abc import abstractmethod
from typing import Type, TypeVar, cast

from .....Tools.AbstractClasses import UniqueObjectABC
from .....Tools.Logger import Logger
from ..Command import CommandABC

T = TypeVar("T", bound=CommandABC.Response)


class BackendABC(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.__LoggerInstance: Logger = LoggerInstance
        self.__IsRunning: bool = False

    def GetLogger(self) -> Logger:
        return self.__LoggerInstance

    def IsRunning(self) -> bool:
        return self.__IsRunning

    def __CheckRunning(self):
        if self.__IsRunning == False:
            raise Exception("You must start the backend before interacting")

    @abstractmethod
    def StartBackend(self):
        self.__IsRunning = True

    @abstractmethod
    def StopBackend(self):
        self.__IsRunning = False

    @abstractmethod
    def ExecuteCommand(self, CommandInstance: CommandABC):
        self.__CheckRunning()

    @abstractmethod
    def GetStatus(self, CommandInstance: CommandABC) -> CommandABC.Response:
        self.__CheckRunning()

    @abstractmethod
    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        self.__CheckRunning()

    @abstractmethod
    def GetResponse(self, CommandInstance: CommandABC, ResponseType: Type[T]) -> T:
        self.__CheckRunning()
