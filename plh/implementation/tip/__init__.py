from __future__ import annotations

from .hamilton_ee_ftr_1000uL import HamiltonEEFTR1000uL
from .hamilton_ee_ntr import HamiltonEENTR
from .hamilton_ee_tip_base import EETipStack, HamiltonEETipBase
from .hamilton_ftr import HamiltonFTR
from .hamilton_ntr import HamiltonNTR
from .pydantic_validators import validate_instance
from .tip_base import TipBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_device_config as _load_device_config

from . import exceptions

identifier = str
devices: dict[identifier, TipBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_device_config(json, TipBase, devices)


def register(device: TipBase)-> None:
    global devices
    devices[device.identifier] = device


def unregister(device: TipBase)-> None:
    del devices[device.identifier]


def unregister_all()-> None:
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
