from __future__ import annotations

from dataclasses import dataclass

from plh.hal.exceptions import HALError

from .tip_base import TipBase


@dataclass
class TierOutOfTipsError(HALError):
    """The Tip device has no more tips available in the teir. A tip discard / reload event is required."""

    error_device: TipBase

    def __str__(self: TierOutOfTipsError) -> str:
        return self.error_device.identifier
