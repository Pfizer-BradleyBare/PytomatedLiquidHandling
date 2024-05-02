from __future__ import annotations

from .hamilton_50uL_core8 import Hamilton50uLCORE8
from .volume_measure_base import VolumeMeasureBase

__all__ = ["VolumeMeasureBase", "Hamilton50uLCORE8"]

identifier = str
devices: dict[identifier, VolumeMeasureBase] = {}
