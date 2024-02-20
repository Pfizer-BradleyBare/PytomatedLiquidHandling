from __future__ import annotations

from dataclasses import dataclass

from plh.hal.exceptions import HALError

from .carrier_base import CarrierBase


@dataclass
class CarrierNotSupportedError(HALError):
    """HAL device does not support your carrier.
    This can be thrown for any LayoutItem inputs.
    """

    carrier: CarrierBase
    """CarrierBase object that is not supported."""

    def __str__(self) -> str:
        return self.carrier.identifier
