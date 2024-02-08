from __future__ import annotations

from dataclasses import dataclass

from plh.hal.exceptions import HALError


@dataclass
class TierOutOfTipsError(HALError):
    """The Tip device has no more tips available in the teir. A tip discard / reload event is required."""

    def __str__(self) -> str:
        return self.error_device.identifier
