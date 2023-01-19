from abc import abstractmethod
from threading import Event
from typing import Callable, Self

from ....Tools.AbstractClasses import ObjectABC
from .Response.Response import Response


class Command(ObjectABC):
    def __init__(
        self,
        Name: str,
        CustomErrorHandlingFunction: Callable[[Self], None] | None,
        CallbackFunction: Callable[[Self, tuple], None] | None,
        CallbackArgs: tuple,
    ):
        self.Name: str = Name
        self.CustomErrorHandlingFunction: Callable[
            [Self], None
        ] | None = CustomErrorHandlingFunction

        self.ResponseInstance: Response | None = None
        self.ResponseEvent: Event = Event()

        self.CallbackFunction: Callable[
            [Command, tuple], None
        ] | None = CallbackFunction

        self.CallbackArgs: tuple = CallbackArgs

    def GetName(self) -> str:
        return self.Name

    def GetResponse(self) -> Response:
        if self.ResponseInstance is None:
            raise Exception("Response not set. Did the command timeout?")

        return self.ResponseInstance

    @abstractmethod
    def GetModuleName(self) -> str:
        ...

    @abstractmethod
    def GetCommandName(self) -> str:
        ...

    @abstractmethod
    def GetResponseKeys(self) -> list[str]:
        ...

    @abstractmethod
    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        ...
