from __future__ import annotations

from .carrier_location_base import CarrierLocationBase
from .non_transportable_carrier_location import NonTransportableCarrierLocation
from .pydantic_validators import validate_instance, validate_list
from .transport_config import TransportConfig
from .transportable_carrier_location import TransportableCarrierLocation

if True:
    """Above needs to be imported first!"""


from plh.implementation.tools import load_resource_config as _load_resource_config

from . import exceptions

identifier = str
devices: dict[identifier, CarrierLocationBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, CarrierLocationBase, devices)


def register(device: CarrierLocationBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: CarrierLocationBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "CarrierLocationBase",
    "NonTransportableCarrierLocation",
    "TransportableCarrierLocation",
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
