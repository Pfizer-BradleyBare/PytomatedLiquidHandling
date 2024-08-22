from __future__ import annotations

from . import hamilton_venus
from .pydantic_validators import validate_instance
from .tip_base import TipBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

from . import exceptions

identifier = str
devices: dict[identifier, TipBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, TipBase, devices)


def register(device: TipBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: TipBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "TipBase",
    "hamilton_venus",
    "exceptions",
    "validate_instance",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
