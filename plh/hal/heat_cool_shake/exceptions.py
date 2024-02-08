from __future__ import annotations

from dataclasses import dataclass

from plh.hal.exceptions import HALError


@dataclass
class HeatingNotSupportedError(HALError):
    """Selected HeatCoolShakeDevice does not support heating."""


@dataclass
class CoolingNotSupportedError(HALError):
    """Selected HeatCoolShakeDevice does not support cooling."""


@dataclass
class ShakingNotSupportedError(HALError):
    """Selected HeatCoolShakeDevice does not support shaking."""
