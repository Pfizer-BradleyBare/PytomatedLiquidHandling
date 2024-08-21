from __future__ import annotations

from .labware_base import LabwareBase
from .layout import AlphanumericLayout, Layout, LayoutSorting, NumericLayout
from .non_pipettable_labware import NonPipettableLabware
from .pipettable_labware import PipettableLabware
from .pydantic_validators import validate_instance, validate_list

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

from . import exceptions

identifier = str
devices: dict[identifier, LabwareBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, LabwareBase, devices)


def register(device: LabwareBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: LabwareBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "LabwareBase",
    "Layout",
    "AlphanumericLayout",
    "NumericLayout",
    "LayoutSorting",
    "NonPipettableLabware",
    "PipettableLabware",
    "exceptions",
    "validate_instance",
    "validate_list",
    "exceptions",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
