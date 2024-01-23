from __future__ import annotations

from .carrier_config import CarrierConfig
from .deck_location_base import DeckLocationBase
from .exceptions import (
    DeckLocationNotSupportedError,
    DeckLocationNotTransportableError,
    DeckLocationTransportConfigsNotCompatibleError,
)
from .non_transportable_deck_location import NonTransportableDeckLocation
from .transport_config import TransportConfig
from .transportable_deck_location import TransportableDeckLocation

__all__ = [
    "DeckLocationBase",
    "CarrierConfig",
    "NonTransportableDeckLocation",
    "TransportableDeckLocation",
    "TransportConfig",
    "DeckLocationNotSupportedError",
    "DeckLocationNotTransportableError",
    "DeckLocationTransportConfigsNotCompatibleError",
]

identifier = str
devices: dict[identifier, DeckLocationBase] = {}
