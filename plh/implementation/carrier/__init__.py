from __future__ import annotations

from .carrier_base import CarrierBase
from .hamilton_autoload_carrier import HamiltonAutoloadCarrier
from .moveable_carrier import MoveableCarrier
from .non_moveable_carrier import NonMoveableCarrier
from .pydantic_validators import validate_instance, validate_list

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_device_config as _load_device_config

from . import exceptions

identifier = str
devices: dict[identifier, CarrierBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_device_config(json, CarrierBase, devices)


def register(device: CarrierBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: CarrierBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "CarrierBase",
    "NonMoveableCarrier",
    "MoveableCarrier",
    "HamiltonAutoloadCarrier",
    "validate_instance",
    "validate_list",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
