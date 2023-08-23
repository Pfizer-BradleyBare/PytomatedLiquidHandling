from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import Carrier


@dataclass
class CarrierConfig:
    CarrierInstance: Carrier.BaseCarrier.CarrierABC
    CarrierPosition: int
