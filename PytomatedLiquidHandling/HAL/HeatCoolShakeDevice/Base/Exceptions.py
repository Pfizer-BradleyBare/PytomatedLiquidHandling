from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .HeatCoolShakeDeviceABC import HeatCoolShakeDeviceABC


@dataclass
class HeatingNotSupportedError(BaseException):
    """Selected HeatCoolShakeDevice does not support heating.

    Attributes:
    None
    """


@dataclass
class CoolingNotSupportedError(BaseException):
    """Selected HeatCoolShakeDevice does not support cooling.

    Attributes:
    None
    """


@dataclass
class ShakingNotSupportedError(BaseException):
    """Selected HeatCoolShakeDevice does not support shaking.

    Attributes:
    None
    """
