from .....Tools.Logger import Logger
from ..BaseHamiltonBackend import HamiltonBackendABC
from ..HamiltonCommand import HamiltonCommandABC


class MicrolabStarBackend(HamiltonBackendABC):
    def __init__(self, UniqueIdentifier: str, LoggerInstance: Logger):
        HamiltonBackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
            "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Hamilton\\Method\\BasicMethod.med",
        )

    def GetStatus(self) -> HamiltonCommandABC.Response:
        ...
