from __future__ import annotations

from pydantic import dataclasses

from .well_segment import WellSegment


@dataclasses.dataclass(kw_only=True)
class Well:
    """Description of labware wells."""

    positions_per_well: int
    """Total number of channels that can fit into the well simultaneously. Ex. Reagent Reservoir has a large well and 8 channels can fit. A fliptube is a smalll well so 1 channel can fit only."""

    max_volume: float
    """Max volume of the well. This may be more or less than the volume described by ```segments```."""

    dead_volume: float
    """Minimum volume required for accurate pipetting from a well."""

    segments: list[WellSegment]
    """Segments which mathmatically describe a well."""
