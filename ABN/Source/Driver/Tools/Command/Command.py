from abc import abstractmethod

from ....Tools.AbstractClasses import ObjectABC
from .Response.Response import Response


class Command(ObjectABC):
    def __init__(self, ResponseInstance: Response):
        self.ResponseInstance: Response = ResponseInstance

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
