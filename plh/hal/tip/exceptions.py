from __future__ import annotations

from dataclasses import dataclass

from .tip_base import TipBase


@dataclass
class TierOutOfTipsError(Exception):
    """The Tip device has no more tips available in the teir. A tip discard / reload event is required."""

    tip: TipBase
    """Tip device that is out of tips in the teir."""

    def __str__(self) -> str:
        return self.tip.identifier
