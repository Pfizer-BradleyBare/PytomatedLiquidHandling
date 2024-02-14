from __future__ import annotations

from .carrier_base import CarrierBase
from .hamilton_autoload_carrier import HamiltonAutoloadCarrier
from .moveable_carrier import MoveableCarrier
from .non_moveable_carrier import NonMoveableCarrier

__all__ = [
    "CarrierBase",
    "NonMoveableCarrier",
    "MoveableCarrier",
    "HamiltonAutoloadCarrier",
]

identifier = str
devices: dict[identifier, CarrierBase] = {}
