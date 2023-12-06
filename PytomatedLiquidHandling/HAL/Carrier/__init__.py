from . import Base
from .AutoloadCarrier import AutoloadCarrier
from .MoveableCarrier import MoveableCarrier
from .NonMoveableCarrier import NonMoveableCarrier

Identifier = str
Devices: dict[Identifier, Base.CarrierABC] = dict()
