from __future__ import annotations

from .labware_base import LabwareBase
from .layout import AlphanumericLayout, Layout, LayoutSorting, NumericLayout
from .non_pipettable_labware import NonPipettableLabware
from .pipettable_labware import PipettableLabware
from .pydantic_validators import validate_instance, validate_list

if True:
    from . import exceptions

from plh.implementation.tools import load_device_list_config as _load_device_list_config

identifier = str
devices: dict[identifier, LabwareBase] = {}


def load(json: dict[str, list[dict]]) -> dict[identifier, LabwareBase]:
    return _load_device_list_config(json, LabwareBase, devices)


def register(device: LabwareBase):
    global devices
    devices[device.identifier] = device


def unregister(device: LabwareBase):
    del devices[device.identifier]


def unregister_all():
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
