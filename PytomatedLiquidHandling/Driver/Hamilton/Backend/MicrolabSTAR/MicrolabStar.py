from ..BaseHamiltonBackend import HamiltonBackendABC
from dataclasses import dataclass, field


@dataclass
class MicrolabStarBackend(HamiltonBackendABC):
    MethodPath: str = field(
        init=False,
        default="C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Hamilton\\Method\\BasicMethod.med",
    )
    DeckLayoutPath: str = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Hamilton\\Method\\Layout\\ExampleLayout.lay"
