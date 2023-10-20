from . import Base
from .AutoloadCarrier import AutoloadCarrier
from .MoveableCarrier import MoveableCarrier
from .NonMoveableCarrier import NonMoveableCarrier

__Objects: dict[str, Base.CarrierABC] = dict()


def GetObjects() -> dict[str, Base.CarrierABC]:
    return __Objects
