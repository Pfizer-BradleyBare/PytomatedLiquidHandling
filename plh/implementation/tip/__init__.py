from __future__ import annotations

from .hamilton_ee_ftr_1000uL import HamiltonEEFTR1000uL
from .hamilton_ee_ntr import HamiltonEENTR
from .hamilton_ee_tip_base import EETipStack, HamiltonEETipBase
from .hamilton_ftr import HamiltonFTR
from .hamilton_ntr import HamiltonNTR
from .pydantic_validators import validate_instance
from .tip_base import TipBase

if True:
    from . import exceptions

from plh.implementation.tools import load_device_config as _load_device_config

identifier = str
devices: dict[identifier, TipBase] = {}


def load(json: dict[str, list[dict]]) -> dict[identifier, TipBase]:
    return _load_device_config(json, TipBase, devices)


def register(device: TipBase):
    global devices
    devices[device.identifier] = device


def unregister(device: TipBase):
    del devices[device.identifier]


def unregister_all():
    global devices
    devices = {}


__all__ = [
    "TipBase",
    "HamiltonFTR",
    "HamiltonNTR",
    "HamiltonEETipBase",
    "HamiltonEEFTR1000uL",
    "HamiltonEENTR",
    "EETipStack",
    "exceptions",
    "validate_instance",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
