from __future__ import annotations

from .coverable_filter_plate import CoverableFilterPlate
from .coverable_plate import CoverablePlate
from .filter_plate import FilterPlate
from .filter_plate_stack import FilterPlateStack
from .layout_item_base import LayoutItemBase
from .lid import Lid
from .plate import Plate
from .tip_rack import TipRack
from .vacuum_manifold import VacuumManifold

__all__ = [
    "LayoutItemBase",
    "CoverableFilterPlate",
    "CoverablePlate",
    "FilterPlate",
    "FilterPlateStack",
    "Lid",
    "Plate",
    "TipRack",
    "VacuumManifold",
]

identifier = str
devices: dict[identifier, LayoutItemBase] = {}
