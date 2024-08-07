from __future__ import annotations

from .coverable_filter_plate import CoverableFilterPlate
from .coverable_plate import CoverablePlate
from .filter_plate import FilterPlate
from .filter_plate_stack import FilterPlateStack
from .layout_item_base import LayoutItemBase
from .lid import Lid
from .plate import Plate
from .pydantic_validators import validate_instance, validate_list
from .tip_rack import TipRack
from .vacuum_manifold import VacuumManifold

if True:
    ...

from plh.implementation.tools import load_device_list_config as _load_device_list_config

identifier = str
devices: dict[identifier, LayoutItemBase] = {}


def load(json: dict[str, list[dict]]) -> dict[identifier, LayoutItemBase]:
    return _load_device_list_config(json, LayoutItemBase, devices)


def register(device: LayoutItemBase):
    global devices
    devices[device.identifier] = device


def unregister(device: LayoutItemBase):
    del devices[device.identifier]


def unregister_all():
    global devices
    devices = {}


__all__ = [
    "LayoutItemBase",
    "TipRack",
    "VacuumManifold",
    "Plate",
    "CoverablePlate",
    "Lid",
    "FilterPlateStack",
    "FilterPlate",
    "CoverableFilterPlate",
    "validate_list",
    "validate_instance",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
