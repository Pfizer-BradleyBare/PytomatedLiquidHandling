from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from plh.hal.exceptions import UserInputRequiredError

from .tip_base import AvailablePosition, TipBase


@dataclass
class TierOutOfTipsError(UserInputRequiredError):
    """The Tip device has no more tips available in the teir. A tip discard / reload event is required."""

    error_device: TipBase

    def __str__(self) -> str:
        return self.error_device.identifier

    def kwargs(self: TierOutOfTipsError) -> dict[str, type]:
        return {"available_positions": AvailablePosition}

    def callback(self: TierOutOfTipsError, **kwargs: dict[str, Any]) -> None:
        # TODO
        ...
