from dataclasses import dataclass

from ....Carrier import CarrierABC


@dataclass
class CarrierConfig:
    CarrierInstance: CarrierABC
    CarrierPosition: int
