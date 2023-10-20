from ..BaseHamiltonBackend import HamiltonBackendABC
from pydantic import PrivateAttr


class MicrolabSTAR(HamiltonBackendABC):
    MethodPath: str = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Hamilton\\Method\\BasicMethod.med"

    DeckLayoutPath: str = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Hamilton\\Method\\Layout\\ExampleLayout.lay"
