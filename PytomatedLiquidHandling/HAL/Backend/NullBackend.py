from dataclasses import dataclass, field
from typing import Type, TypeVar

from ...Driver.Tools.AbstractClasses import BackendABC, CommandABC, ResponseABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclass
class NullBackend(BackendABC):
    Identifier: str | int = field(init=False, default="Null Backend")
    LoggerInstance: None = field(init=False, default=None)

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
