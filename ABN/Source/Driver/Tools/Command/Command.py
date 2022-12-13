from abc import abstractmethod
from threading import Event

from ....Tools.AbstractClasses import ObjectABC
from .Response.Response import Response


class Command(ObjectABC):
    def __init__(self, Name: str, CustomErrorHandling: bool):
        self.ResponseInstance: Response | None = None
        self.ResponseEvent: Event = Event()
        self.Name: str = Name
        self.CustomErrorHandling: bool = CustomErrorHandling

    def GetName(self) -> str:
        return self.Name

    def GetResponse(self) -> Response:
        if self.ResponseInstance is None:
            raise Exception("Response not set. Did the command timeout?")

        return self.ResponseInstance

    @abstractmethod
    def GetModuleName(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def GetCommandName(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def GetResponseKeys(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        raise NotImplementedError
