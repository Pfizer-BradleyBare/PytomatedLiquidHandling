from __future__ import annotations

from .hamilton_portrait_core8 import HamiltonPortraitCORE8
from .hamilton_portrait_core8_contact_dispense import (
    HamiltonPortraitCORE8ContactDispense,
)
from .hamilton_portrait_core8_simple_contact_dispense import (
    HamiltonPortraitCORE8SimpleContactDispense,
)

if True:
    pass
# This MUST come first so the if statement ensures that it does not get reordered by a formatter

# from .hamilton_core96 import HamiltonCORE96
from .liquid_class import LiquidClass
from .options import AspirateOptions, DispenseOptions
from .pipette_base import PipetteBase
from .pipette_tip import PipetteTip
from .pydantic_validators import validate_instance

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_device_config as _load_device_config

from . import exceptions

identifier = str
devices: dict[identifier, PipetteBase] = {}

def load(json: dict[str, list[dict]])  -> None:
    _load_device_config(json, PipetteBase, devices)


def register(device: PipetteBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: PipetteBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "PipetteBase",
    "PipetteTip",
    "LiquidClass",
    "AspirateOptions",
    "DispenseOptions",
    "_AspirateDispenseOptions",
    "validate_instance",
    "HamiltonPortraitCORE8",
    "HamiltonPortraitCORE8ContactDispense",
    "HamiltonPortraitCORE8SimpleContactDispense",
    "HamiltonCORE96",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
