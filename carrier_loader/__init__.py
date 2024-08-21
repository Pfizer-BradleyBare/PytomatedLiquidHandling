from __future__ import annotations

from .carrier_loader_base import CarrierLoaderBase
from .hamilton_star_autoload import HamiltonStarAutoload
from .hamilton_vantage_autoload import HamiltonVantageAutoload

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

identifier = str
devices: dict[identifier, CarrierLoaderBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, CarrierLoaderBase, devices)


def register(device: CarrierLoaderBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: CarrierLoaderBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "CarrierLoaderBase",
    "HamiltonStarAutoload",
    "HamiltonVantageAutoload",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
