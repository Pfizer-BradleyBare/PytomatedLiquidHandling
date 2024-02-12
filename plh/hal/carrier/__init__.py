from __future__ import annotations

from .carrier_base import CarrierBase
from .moveable_carrier import MoveableCarrier
from .non_moveable_carrier import NonMoveableCarrier

__all__ = ["CarrierBase", "NonMoveableCarrier", "MoveableCarrier", "AutoloadCarrier"]

identifier = str
devices: dict[identifier, CarrierBase] = {}
