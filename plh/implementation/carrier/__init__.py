from __future__ import annotations

from .carrier_base import CarrierBase
from .generic_automatic_move_carrier import GenericAutomaticMoveCarrier
from .generic_manual_move_carrier import GenericManualMoveCarrier
from .generic_stationary_carrier import GenericStationaryCarrier
from .pydantic_validators import validate_instance, validate_list

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
    "GenericStationaryCarrier",
    "GenericManualMoveCarrier",
    "GenericAutomaticMoveCarrier",
    "validate_instance",
    "validate_list",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
