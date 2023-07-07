from dataclasses import dataclass

from ...Driver.Hamilton.Backend import VantageBackend
from .BaseTransportDevice import (
    DeckLocationTransportConfig,
    TransportDevice,
    TransportOptions,
)


@dataclass
class VantageTrackGripper(TransportDevice):
    BackendInstance: VantageBackend

    class GetConfig(DeckLocationTransportConfig.TransportConfigABC):
        def __init__(self, Config: dict):
            ...

        def _ComparisonKeys(self) -> list[str]:
            return []

    class PlaceConfig(DeckLocationTransportConfig.TransportConfigABC):
        def __init__(self, Config: dict):
            ...

        def _ComparisonKeys(self) -> list[str]:
            return []

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...
