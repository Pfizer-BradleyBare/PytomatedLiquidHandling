from __future__ import annotations

from .hamilton_50uL_core8 import Hamilton50uLCORE8
from .volume_measure_base import VolumeMeasureBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

identifier = str
devices: dict[identifier, VolumeMeasureBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, VolumeMeasureBase, devices)


def register(device: VolumeMeasureBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: VolumeMeasureBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "VolumeMeasureBase",
    "Hamilton50uLCORE8",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
