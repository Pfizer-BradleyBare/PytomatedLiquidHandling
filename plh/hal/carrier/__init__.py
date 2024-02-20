from __future__ import annotations

from .carrier_base import CarrierBase
from .hamilton_autoload_carrier import HamiltonAutoloadCarrier
from .moveable_carrier import MoveableCarrier
from .non_moveable_carrier import NonMoveableCarrier
from .pydantic_validators import validate_instance, validate_list

if True:
    """Exceptions always come last."""

from . import exceptions

__all__ = [
    "CarrierBase",
    "NonMoveableCarrier",
    "MoveableCarrier",
    "HamiltonAutoloadCarrier",
    "validate_instance",
    "validate_list",
    "exceptions",
]

identifier = str
devices: dict[identifier, CarrierBase] = {}
