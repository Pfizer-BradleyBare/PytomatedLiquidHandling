from __future__ import annotations

from .deck_location_base import DeckLocationBase
from .non_transportable_deck_location import NonTransportableDeckLocation
from .pydantic_validators import validate_instance, validate_list
from .transport_config import TransportConfig
from .transportable_deck_location import TransportableDeckLocation

if True:
    from . import exceptions

__all__ = [
    "DeckLocationBase",
    "NonTransportableDeckLocation",
    "TransportableDeckLocation",
    "TransportConfig",
    "exceptions",
    "validate_instance",
    "validate_list",
]

identifier = str
devices: dict[identifier, DeckLocationBase] = {}
