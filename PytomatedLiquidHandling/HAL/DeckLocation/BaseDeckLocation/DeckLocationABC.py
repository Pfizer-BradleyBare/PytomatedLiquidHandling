from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .CarrierConfig import CarrierConfig


@dataclass
class DeckLocationABC(UniqueObjectABC):
    CarrierConfigInstance: CarrierConfig
