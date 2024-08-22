from __future__ import annotations

from . import hamilton_venus
from .vacuum_base import FilterPlateConfiguration, VacuumBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

identifier = str
devices: dict[identifier, VacuumBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, VacuumBase, devices)


def register(device: VacuumBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: VacuumBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "VacuumBase",
    "FilterPlateConfiguration",
    "hamilton_venus",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
