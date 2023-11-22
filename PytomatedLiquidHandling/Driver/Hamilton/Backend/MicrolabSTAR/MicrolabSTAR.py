from pydantic import PrivateAttr

from ..BaseHamiltonBackend import HamiltonBackendABC


class MicrolabSTAR(HamiltonBackendABC):
    MethodPath: str = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Method\\BasicMethod.med"

    DeckLayoutPath: str = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\MicrolabSTAR\\Method\\ExampleLayout.lay"
