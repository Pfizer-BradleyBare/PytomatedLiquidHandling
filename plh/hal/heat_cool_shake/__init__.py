from __future__ import annotations

from .exceptions import (
    CoolingNotSupportedError,
    HeatingNotSupportedError,
    ShakingNotSupportedError,
)
from .hamilton_heater_cooler import HamiltonHeaterCooler
from .hamilton_heater_shaker import HamiltonHeaterShaker
from .heat_cool_shake_base import HeatCoolShakeBase

__all__ = [
    "HeatCoolShakeBase",
    "HamiltonHeaterShaker",
    "HamiltonHeaterCooler",
    "HeatingNotSupportedError",
    "CoolingNotSupportedError",
    "ShakingNotSupportedError",
]
identifier = str
devices: dict[identifier, HeatCoolShakeBase] = {}
