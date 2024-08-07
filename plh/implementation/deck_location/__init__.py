from __future__ import annotations

from .deck_location_base import DeckLocationBase
from .non_transportable_deck_location import NonTransportableDeckLocation
from .pydantic_validators import validate_instance, validate_list
from .transport_config import TransportConfig
from .transportable_deck_location import TransportableDeckLocation

if True:
    from . import exceptions

from plh.implementation.tools import load_device_config as _load_device_config

identifier = str
devices: dict[identifier, DeckLocationBase] = {}


def load(json: dict[str, list[dict]]) -> dict[identifier, DeckLocationBase]:
    return _load_device_config(json, DeckLocationBase, devices)


def register(device: DeckLocationBase):
    global devices
    devices[device.identifier] = device


def unregister(device: DeckLocationBase):
    del devices[device.identifier]


def unregister_all():
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
