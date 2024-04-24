from __future__ import annotations

from dataclasses import dataclass

from plh.implementation.exceptions import HALError

from .heat_cool_shake_base import HeatCoolShakeBase


@dataclass
class HeatingNotSupportedError(HALError):
    """Selected HeatCoolShakeDevice does not support heating."""

    error_device: HeatCoolShakeBase


@dataclass
class CoolingNotSupportedError(HALError):
    """Selected HeatCoolShakeDevice does not support cooling."""

    error_device: HeatCoolShakeBase


@dataclass
class ShakingNotSupportedError(HALError):
    """Selected HeatCoolShakeDevice does not support shaking."""

    error_device: HeatCoolShakeBase
