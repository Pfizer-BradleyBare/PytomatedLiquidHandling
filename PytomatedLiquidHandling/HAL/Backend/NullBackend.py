from dataclasses import dataclass
from typing import Type, TypeVar

from ...Driver.Tools.AbstractClasses import BackendABC, CommandABC

T = TypeVar("T", bound=CommandABC.Response)


@dataclass
class NullBackend(BackendABC):
    def StartBackend(self):
        ...

    def StopBackend(self):
        ...

    def ExecuteCommand(self, CommandInstance: CommandABC):
        ...

    def GetCommandStatus(self, CommandInstance: CommandABC) -> CommandABC.Response:
        ...

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        ...

    def GetResponse(self, CommandInstance: CommandABC, ResponseType: Type[T]) -> T:
        ...
