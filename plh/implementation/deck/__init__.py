from . import hamilton_venus
from .deck_base import DeckBase
from .liquid_handler_deck_base import LiquidHandlerDeckBase
from .pydantic_validators import validate_instance

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

identifier = str
devices: dict[identifier, DeckBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, DeckBase, devices)


def register(device: DeckBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: DeckBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "DeckBase",
    "LiquidHandlerDeckBase",
    "hamilton_venus",
    "validate_instance",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
