from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Type, TypeVar

from PytomatedLiquidHandling.Tools import AbstractClasses, Logger

from ..Command import CommandABC
from ..Exception import ExceptionABC
from ..Response import ResponseABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclass
class BackendABC(AbstractClasses.UniqueObjectABC):
    LoggerInstance: Logger.Logger
    IsRunning: bool = field(init=False, default=False)
    Exceptions: list[type[ExceptionABC]] = field(init=False, default_factory=list)

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
    def GetCommandStatus(self, CommandInstance: CommandABC) -> ResponseABC:
        self.__CheckRunning()

    @abstractmethod
    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        self.__CheckRunning()

    @abstractmethod
    def GetResponse(
        self, CommandInstance: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
        self.__CheckRunning()
