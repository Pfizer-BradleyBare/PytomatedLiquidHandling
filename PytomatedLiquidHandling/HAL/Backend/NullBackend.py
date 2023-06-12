from dataclasses import dataclass
from typing import Type, TypeVar

from ...Driver.Tools.AbstractClasses import BackendABC, CommandABC, ResponseABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclass
class NullBackend(BackendABC):
    def StartBackend(self):
        ...

    def StopBackend(self):
        ...

    def ExecuteCommand(self, CommandInstance: CommandABC):
        ...

    def GetCommandStatus(self, CommandInstance: CommandABC) -> ResponseABC:
        ...

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        ...

    def GetResponse(
        self, CommandInstance: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
        ...
