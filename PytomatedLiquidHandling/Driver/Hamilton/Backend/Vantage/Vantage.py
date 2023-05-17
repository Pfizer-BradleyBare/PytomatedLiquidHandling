from .....Tools.Logger import Logger
from ..BaseHamiltonBackend import HamiltonBackendABC
from ..HamiltonCommand import HamiltonCommandABC


class VantageBackend(HamiltonBackendABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger):
        HamiltonBackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
        )

    def GetStatus(self) -> HamiltonCommandABC.Response:
        ...
