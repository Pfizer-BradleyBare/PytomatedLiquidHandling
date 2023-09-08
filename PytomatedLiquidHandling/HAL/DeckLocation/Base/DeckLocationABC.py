from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from .CarrierConfig import CarrierConfig
from .TransportConfig import TransportConfig


@dataclass
class DeckLocationABC(HALObject):
    CarrierConfig: CarrierConfig
    TransportConfig: TransportConfig
