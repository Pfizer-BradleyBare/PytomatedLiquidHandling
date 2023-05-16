from ..BaseHamiltonBackend import HamiltonBackendABC
from ..HamiltonCommand import HamiltonCommandABC
from .....Tools.Logger import Logger


class VantageBackend(HamiltonBackendABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger, Port: int = 7286):
        HamiltonBackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
            "/Hamilton/Vantage/",
            Port=Port,
        )

    @HamiltonBackendABC.Decorator_ExecuteCommand
    def ExecuteCommand(self, CommandInstance: HamiltonCommandABC):
        ...

    def GetStatus(self) -> HamiltonCommandABC.Response:
        ...
