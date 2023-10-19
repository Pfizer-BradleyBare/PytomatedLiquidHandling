from pydantic.dataclasses import dataclass

from .MoveableCarrier import MoveableCarrier


@dataclass
class AutoloadCarrier(MoveableCarrier):
    CarrierLabwareID: str
