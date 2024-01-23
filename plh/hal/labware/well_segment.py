from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class WellSegment:
    """A segment in a well definition."""

    height: float
    """Height of the segment."""

    equation: str
    """Equation that describes the segment."""
