from __future__ import annotations

from .carrier_config import CarrierConfig
from .deck_location_base import DeckLocationBase
from .non_transportable_deck_location import NonTransportableDeckLocation
from .transport_config import TransportConfig
from .transportable_deck_location import TransportableDeckLocation

if True:
    from . import exceptions

__all__ = [
    "DeckLocationBase",
    "CarrierConfig",
    "NonTransportableDeckLocation",
    "TransportableDeckLocation",
    "TransportConfig",
    "exceptions",
]

identifier = str
devices: dict[identifier, DeckLocationBase] = {}
