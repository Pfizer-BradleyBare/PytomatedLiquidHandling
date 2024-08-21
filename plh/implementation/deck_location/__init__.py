from __future__ import annotations

from .deck_location_base import DeckLocationBase
from .non_transportable_deck_location import NonTransportableDeckLocation
from .pydantic_validators import validate_instance, validate_list
from .transport_config import TransportConfig
from .transportable_deck_location import TransportableDeckLocation

if True:
    """Above needs to be imported first!"""


from plh.implementation.tools import load_resource_config as _load_resource_config

from . import exceptions

identifier = str
devices: dict[identifier, DeckLocationBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, DeckLocationBase, devices)


def register(device: DeckLocationBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: DeckLocationBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "DeckLocationBase",
    "NonTransportableDeckLocation",
    "TransportableDeckLocation",
    "TransportConfig",
    "exceptions",
    "validate_instance",
    "validate_list",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
