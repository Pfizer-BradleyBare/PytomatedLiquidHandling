from typing import Type, TypeVar
from dataclasses import dataclass
from ...Driver.Tools.AbstractClasses import CommandABC
from ...Driver.Tools.AbstractClasses import BackendABC

T = TypeVar("T", bound=CommandABC.Response)


@dataclass
class NullBackend(BackendABC):
    def StartBackend(self):
        ...

    def StopBackend(self):
        ...

    def ExecuteCommand(self, CommandInstance: CommandABC):
        ...

    def GetStatus(self, CommandInstance: CommandABC) -> CommandABC.Response:
        ...

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        ...

    def GetResponse(self, CommandInstance: CommandABC, ResponseType: Type[T]) -> T:
        ...
