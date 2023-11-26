from abc import abstractmethod
from typing import Type, TypeVar

from pydantic import PrivateAttr, BaseModel

from PytomatedLiquidHandling.HAL.Tools import AbstractClasses

from ..Command import CommandABC
from ..Response import ResponseABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


class CommandStatusResponse(ResponseABC):
    ResponseReady: bool


class BackendABC(BaseModel):
    Identifier: str
    _IsRunning: bool = PrivateAttr(default=False)

    def __CheckRunning(self):
        if self._IsRunning == False:
            raise RuntimeError("You must start the backend before interacting")

    @abstractmethod
    def StartBackend(self):
        self._IsRunning = True

    @abstractmethod
    def StopBackend(self):
        self._IsRunning = False

    @abstractmethod
    def ExecuteCommand(self, CommandInstance: CommandABC):
        self.__CheckRunning()

    @abstractmethod
    def GetCommandStatus(self, CommandInstance: CommandABC) -> CommandStatusResponse:
        self.__CheckRunning()

    @abstractmethod
    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        self.__CheckRunning()

    @abstractmethod
    def GetResponse(
        self, CommandInstance: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
        self.__CheckRunning()
