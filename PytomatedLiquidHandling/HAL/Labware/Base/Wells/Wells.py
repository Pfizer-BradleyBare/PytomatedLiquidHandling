from pydantic import dataclasses

from .Layout import AlphaNumeric, Numeric
from .Segment import Segment


@dataclasses.dataclass(kw_only=True)
class Wells:
    Layout: AlphaNumeric | Numeric
    PositionsPerWell: int
    MaxVolume: float
    DeadVolume: float
    Segments: list[Segment]
