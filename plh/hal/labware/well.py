from __future__ import annotations

from pydantic import dataclasses

from .well_segment import WellSegment


@dataclasses.dataclass(kw_only=True)
class Well:
    positions_per_well: int
    max_volume: float
    dead_volume: float
    segments: list[WellSegment]
