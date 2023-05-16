from .....Tools.Logger import Logger
from ..BaseHamiltonBackend import HamiltonBackendABC
from ..HamiltonCommand import HamiltonCommandABC


class VantageBackend(HamiltonBackendABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger, Port: int = 7286):
        HamiltonBackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
            "/Hamilton/Vantage/",
            Port=Port,
        )

    def GetStatus(self) -> HamiltonCommandABC.Response:
        ...
