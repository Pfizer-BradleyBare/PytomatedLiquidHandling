from .....Tools.Logger import Logger
from ..BaseHamiltonBackend import HamiltonBackendABC
from ..HamiltonCommand import HamiltonCommandABC


class VantageBackend(HamiltonBackendABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        LoggerInstance: Logger,
        DeckLayoutPath: str | None = None,
    ):
        if DeckLayoutPath is None:
            DeckLayoutPath = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Hamilton\\Method\\Layout\\ExampleLayout.lay"

        HamiltonBackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
            "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Hamilton\\Method\\BasicMethod.med",
            DeckLayoutPath,
        )
