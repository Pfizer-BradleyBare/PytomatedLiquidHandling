from __future__ import annotations

from . import hamilton_venus
from .coverable_filter_plate_base import CoverableFilterPlateBase
from .coverable_plate_base import CoverablePlateBase
from .filter_plate_base import FilterPlateBase
from .filter_plate_stack_base import FilterPlateStackBase
from .layout_item_base import LayoutItemBase
from .lid_base import LidBase
from .plate_base import PlateBase
from .pydantic_validators import validate_instance, validate_list
from .tip_rack_base import TipRackBase
from .vacuum_manifold_base import VacuumManifoldBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

identifier = str
devices: dict[identifier, LayoutItemBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, LayoutItemBase, devices)


def register(device: LayoutItemBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: LayoutItemBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "LayoutItemBase",
    "TipRackBase",
    "VacuumManifoldBase",
    "PlateBase",
    "CoverablePlateBase",
    "LidBase",
    "FilterPlateStackBase",
    "FilterPlateBase",
    "CoverableFilterPlateBase",
    "hamilton_venus",
    "validate_list",
    "validate_instance",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
