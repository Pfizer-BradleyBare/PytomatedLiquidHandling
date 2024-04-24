from __future__ import annotations

from pydantic import dataclasses

from .calibration_point import CalibrationPoint


@dataclasses.dataclass(kw_only=True)
class Well:
    """Description of labware wells."""

    positions_per_well: int
    """Total number of channels that can fit into the well simultaneously. Ex. Reagent Reservoir has a large well and 8 channels can fit. A fliptube is a smalll well so 1 channel can fit only."""

    max_volume: float
    """Max volume of the well. This may be more or less than the volume described by ```segments```."""

    dead_volume: float
    """Minimum volume required for accurate pipetting from a well."""

    calibration_curve: list[CalibrationPoint]
    """Calibration curve used to mathematically describe a well."""

    def __post_init__(self: Well) -> None:
        self.calibration_curve.append(CalibrationPoint(volume=0, height=0))
        self.calibration_curve = sorted(self.calibration_curve, key=lambda x: x.volume)
