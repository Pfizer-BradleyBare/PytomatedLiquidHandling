from dataclasses import dataclass

from ....Tools.AbstractClasses import UniqueObjectABC
from .CarrierConfig import CarrierConfig


@dataclass
class DeckLocationABC(UniqueObjectABC):
    CarrierConfigInstance: CarrierConfig
