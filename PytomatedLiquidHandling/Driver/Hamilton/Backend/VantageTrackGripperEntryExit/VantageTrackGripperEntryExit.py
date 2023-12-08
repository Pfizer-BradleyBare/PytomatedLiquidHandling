from pydantic import dataclasses

from ..BaseHamiltonBackend import HamiltonBackendABC


@dataclasses.dataclass(kw_only=True)
class VantageTrackGripperEntryExit(HamiltonBackendABC):
    MethodPath: str = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\VantageTrackGripperEntryExit\\Method\\BasicMethod.med"
    DeckLayoutPath: str = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\VantageTrackGripperEntryExit\\Method\\ExampleLayout.lay"
