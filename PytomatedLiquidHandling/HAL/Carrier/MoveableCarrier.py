from dataclasses import dataclass

from .BaseCarrier import CarrierABC


@dataclass
class MoveableCarrier(CarrierABC):
    ...
