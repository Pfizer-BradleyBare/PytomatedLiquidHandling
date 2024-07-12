from __future__ import annotations

from itertools import pairwise

from pydantic import dataclasses
from typing_extensions import TypedDict

from .labware_base import *
from .labware_base import LabwareBase


class CalibrationPoint(TypedDict):
    """A segment in a well definition."""

    volume: float
    """Calibration volume."""

    height: float
    """Calibration height."""


@dataclasses.dataclass(kw_only=True, eq=False)
class PipettableLabware(LabwareBase):
    """Labware type that can be pipetted to/from."""

    positions_per_well: int
    """Total number of channels that can fit into the well simultaneously. Ex. Reagent Reservoir has a large well and 8 channels can fit. A fliptube is a smalll well so 1 channel can fit only."""

    max_volume: float
    """Max volume of the well. This may be more or less than the volume described by ```segments```."""

    dead_volume: float
    """Minimum volume required for accurate pipetting from a well."""

    calibration_curve: list[CalibrationPoint]
    """Calibration curve used to mathematically describe a well."""

    def __post_init__(self: PipettableLabware) -> None:
        self.calibration_curve.append({"volume": 0.0, "height": 0.0})
        self.calibration_curve = sorted(
            self.calibration_curve,
            key=lambda x: x["volume"],
        )

    def interpolate_volume(self: PipettableLabware, volume: float) -> float:
        """Calculates height at a given volume."""
        if volume <= 0:
            return 0

        interpolation_points = list(pairwise(self.calibration_curve))
        # edge case where we may not find points to interpolate. This will extrapolate past the last two points on the curve.

        points = interpolation_points[-1]

        for p1, p2 in interpolation_points:
            v1 = p1["volume"]
            v2 = p2["volume"]

            if v1 <= volume <= v2:
                points = (p1, p2)

        p1, p2 = points

        # NOTE: height is our rise or Y and volume is our run or X

        v1 = p1["volume"]
        h1 = p1["height"]

        v2 = p2["volume"]
        h2 = p2["height"]

        rise = h2 - h1
        run = v2 - v1

        if rise == 0 or run == 0:
            return h1

        m = rise / run
        x = volume - v1
        b = h1

        return m * x + b

    def interpolate_height(self: PipettableLabware, height: float) -> float:
        """Calculates volume at a given height."""
        if height <= 0:
            return 0

        interpolation_points = list(pairwise(self.calibration_curve))
        # edge case where we may not find points to interpolate. This will extrapolate past the last two points on the curve.

        points = interpolation_points[-1]

        for p1, p2 in interpolation_points:
            h1 = p1["height"]
            h2 = p2["height"]

            if h1 <= height <= h2:
                points = (p1, p2)

        p1, p2 = points

        # NOTE: height is our run or X and volume is our rise or Y

        v1 = p1["volume"]
        h1 = p1["height"]

        v2 = p2["volume"]
        h2 = p2["height"]

        rise = v2 - v1
        run = h2 - h1

        if rise == 0 or run == 0:
            return v1

        m = rise / run
        x = height - h1
        b = v1

        return m * x + b
