from __future__ import annotations

from itertools import pairwise

from pydantic import dataclasses

from .labware_base import *
from .labware_base import LabwareBase
from .well import Well


@dataclasses.dataclass(kw_only=True, eq=False)
class PipettableLabware(LabwareBase):
    """Labware type that can be pipetted to/from."""

    well_definition: Well
    """Well object."""

    def interpolate_volume(self: PipettableLabware, volume: float) -> float:
        """Calculates height at a given volume."""
        if volume <= 0:
            return 0

        interpolation_points = list(pairwise(self.well_definition.calibration_curve))
        # edge case where we may not find points to interpolate. This will extrapolate past the last two points on the curve.

        points = interpolation_points[-1]

        for p1, p2 in interpolation_points:
            v1 = p1.volume
            v2 = p2.volume

            if v1 <= volume <= v2:
                points = (p1, p2)

        p1, p2 = points

        # NOTE: height is our rise or Y and volume is our run or X

        v1 = p1.volume
        h1 = p1.height

        v2 = p2.volume
        h2 = p2.height

        rise = h2 - h1
        run = v2 - v1

        if rise == 0 or run == 0:
            return h1

        m = rise / run
        b = h1

        return m * volume + b

    def interpolate_height(self: PipettableLabware, height: float) -> float:
        """Calculates volume at a given height."""
        if height <= 0:
            return 0

        interpolation_points = list(pairwise(self.well_definition.calibration_curve))
        # edge case where we may not find points to interpolate. This will extrapolate past the last two points on the curve.

        points = interpolation_points[-1]

        for p1, p2 in interpolation_points:
            h1 = p1.height
            h2 = p2.height

            if h1 <= height <= h2:
                points = (p1, p2)

        p1, p2 = points

        # NOTE: height is our run or X and volume is our rise or Y

        v1 = p1.volume
        h1 = p1.height

        v2 = p2.volume
        h2 = p2.height

        rise = v2 - v1
        run = h2 - h1

        if rise == 0 or run == 0:
            return v1

        m = rise / run
        b = h1

        return m * height + b
