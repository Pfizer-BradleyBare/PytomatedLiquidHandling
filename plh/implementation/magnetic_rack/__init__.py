from __future__ import annotations

from .magnetic_rack import MagneticRack
from .magnetic_rack_base import MagneticRackBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_device_config as _load_device_config

identifier = str
devices: dict[identifier, MagneticRackBase] = {}

def load(json: dict[str, list[dict]])  -> None:
    _load_device_config(json, MagneticRackBase, devices)


def register(device: MagneticRackBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: MagneticRackBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "MagneticRackBase",
    "MagneticRack",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
