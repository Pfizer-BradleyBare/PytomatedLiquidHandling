from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from .CarrierConfig import CarrierConfig


@dataclass
class DeckLocationABC(HALObject):
    CarrierConfigInstance: CarrierConfig
