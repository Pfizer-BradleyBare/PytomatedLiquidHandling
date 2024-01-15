from __future__ import annotations

from .HeatCoolShakeABC import HeatCoolShakeABC

__all__ = ["HeatCoolShakeABC"]
identifier = str
devices: dict[identifier, HeatCoolShakeABC] = {}
