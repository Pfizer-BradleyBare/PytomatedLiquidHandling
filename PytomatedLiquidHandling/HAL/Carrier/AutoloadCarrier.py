from dataclasses import dataclass

from .MoveableCarrier import MoveableCarrier


@dataclass
class AutoloadCarrier(MoveableCarrier):
    LabwareID: str
