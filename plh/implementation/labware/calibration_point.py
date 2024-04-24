from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class CalibrationPoint:
    """A segment in a well definition."""

    volume: float
    """Calibration volume."""

    height: float
    """Calibration height."""
