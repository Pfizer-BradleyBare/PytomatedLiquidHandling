from pydantic.dataclasses import dataclass

from .Base import CarrierABC


@dataclass
class NonMoveableCarrier(CarrierABC):
    ...
