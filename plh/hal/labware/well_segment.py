from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class WellSegment:
    height: float
    equation: str
