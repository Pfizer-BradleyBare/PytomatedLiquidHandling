from __future__ import annotations

from .carrier_loader_base import CarrierLoaderBase
from .hamilton_star_autoload import HamiltonStarAutoload
from .hamilton_vantage_autoload import HamiltonVantageAutoload

if True:
    """Exceptions always come last."""

from plh.implementation.tools import load_device_config as _load_device_config

identifier = str
devices: dict[identifier, CarrierLoaderBase] = {}


def load(json: dict[str, list[dict]]) -> dict[identifier, CarrierLoaderBase]:
    return _load_device_config(json, CarrierLoaderBase, devices)


def register(device: CarrierLoaderBase):
    global devices
    devices[device.identifier] = device


def unregister(device: CarrierLoaderBase):
    del devices[device.identifier]


def unregister_all():
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
