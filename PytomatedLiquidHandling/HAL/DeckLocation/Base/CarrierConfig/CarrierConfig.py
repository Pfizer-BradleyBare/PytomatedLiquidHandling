from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import Carrier


@dataclass
class CarrierConfig:
    Carrier: Carrier.Base.CarrierABC
    CarrierPosition: int
