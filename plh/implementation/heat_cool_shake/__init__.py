from __future__ import annotations

from .hamilton_heater_cooler import HamiltonHeaterCooler
from .hamilton_heater_shaker import HamiltonHeaterShaker
from .heat_cool_shake_base import HeatCoolShakeBase
from .options import HeatCoolShakeOptions

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

from . import exceptions

identifier = str
devices: dict[identifier, HeatCoolShakeBase] = {}


def load(json: dict[str, list[dict]]) -> dict[identifier, HeatCoolShakeBase]:
    return _load_resource_config(json, HeatCoolShakeBase, devices)


def register(device: HeatCoolShakeBase):
    global devices
    devices[device.identifier] = device


def unregister(device: HeatCoolShakeBase):
    del devices[device.identifier]


def unregister_all():
    global devices
    devices = {}


__all__ = [
    "HeatCoolShakeBase",
    "HamiltonHeaterShaker",
    "HamiltonHeaterCooler",
    "exceptions",
    "HeatCoolShakeOptions",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
