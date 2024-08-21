from __future__ import annotations

from .automatic_move_liquid_handler_carrier import AutomaticMoveLiquidHandlerCarrier
from .carrier_base import CarrierBase
from .manual_move_liquid_handler_carrier import ManualMoveLiquidHandlerCarrier
from .pydantic_validators import validate_instance, validate_list
from .stationary_liquid_handler_carrier import StationaryLiquidHandlerCarrier

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

from . import exceptions

identifier = str
devices: dict[identifier, CarrierBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, CarrierBase, devices)


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
    "StationaryLiquidHandlerCarrier",
    "ManualMoveLiquidHandlerCarrier",
    "AutomaticMoveLiquidHandlerCarrier",
    "validate_instance",
    "validate_list",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
