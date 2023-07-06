from dataclasses import dataclass

from .....Tools.AbstractClasses import UniqueObjectABC


@dataclass
class DeckLocationTransportConfig(UniqueObjectABC):
    GetConfig: dict
    PlaceConfig: dict
