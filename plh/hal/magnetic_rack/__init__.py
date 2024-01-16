from __future__ import annotations

from .magnetic_rack import MagneticRack
from .magnetic_rack_base import MagneticRackBase

__all__ = ["MagneticRackBase", "MagneticRack"]

identifier = str
devices: dict[identifier, MagneticRackBase] = {}
