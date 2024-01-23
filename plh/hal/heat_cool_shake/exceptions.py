from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HeatingNotSupportedError(Exception):
    """Selected HeatCoolShakeDevice does not support heating."""


@dataclass
class CoolingNotSupportedError(Exception):
    """Selected HeatCoolShakeDevice does not support cooling."""


@dataclass
class ShakingNotSupportedError(Exception):
    """Selected HeatCoolShakeDevice does not support shaking."""
