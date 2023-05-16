from ....Tools.AbstractClasses import BackendABC
from ..HamiltonCommand import HamiltonCommandABC


class MicrolabSTAR(BackendABC):
    def __init__(self):
        ...

    def StartBackend(self):
        ...

    def StopBackend(self):
        ...

    @BackendABC.Decorator_ExecuteCommand
    def ExecuteCommand(self, CommandInstance: HamiltonCommandABC):
        ...

    def GetStatus(self) -> HamiltonCommandABC.Response:
        ...
