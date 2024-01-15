from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import dataclasses

if TYPE_CHECKING:
    from .layout import AlphaNumericLayout, NumericLayout
    from .well_segment import WellSegment


@dataclasses.dataclass(kw_only=True)
class Well:
    layout: AlphaNumericLayout | NumericLayout
    positions_per_well: int
    max_volume: float
    dead_volume: float
    segments: list[WellSegment]
