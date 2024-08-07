from __future__ import annotations

from .centrifuge_base import CentrifugeBase
from .hamilton_hig4 import HamiltonHig4

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_device_config as _load_device_config

from . import exceptions

identifier = str
devices: dict[identifier, CentrifugeBase] = {}

def load(json: dict[str, list[dict]]) -> None:
    _load_device_config(json, CentrifugeBase, devices)


def register(device: CentrifugeBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: CentrifugeBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "CentrifugeBase",
    "HamiltonHig4",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
