from abc import abstractmethod
from threading import Event

from ....Tools.AbstractClasses import ObjectABC
from .Response.Response import Response


class Command(ObjectABC):
    def __init__(self, ResponseInstance: Response):
        self.ResponseInstance: Response = ResponseInstance
        self.ResponseEvent: Event = Event()

    def WaitForResponse(self, timeout: float | None = None):
        self.ResponseEvent.wait(timeout)

    def GetResponse(self) -> Response:
        return self.ResponseInstance

    @abstractmethod
    def GetModuleName(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def GetCommandName(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        raise NotImplementedError
