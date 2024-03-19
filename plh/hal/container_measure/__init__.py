from __future__ import annotations

from .container_measure_base import ContainerMeasureBase
from .hamilton_50uL_core8 import Hamilton50uLCORE8

__all__ = ["ContainerMeasureBase", "Hamilton50uLCORE8"]

identifier = str
devices: dict[identifier, ContainerMeasureBase] = {}
