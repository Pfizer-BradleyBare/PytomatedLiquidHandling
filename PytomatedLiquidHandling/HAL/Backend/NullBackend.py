from dataclasses import dataclass, field
from typing import Type, TypeVar

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import CommandABC, ResponseABC

from .Base import BackendABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclass
class NullBackend(BackendABC):
    Identifier: str | int = field(init=False, default="Null Backend")

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
