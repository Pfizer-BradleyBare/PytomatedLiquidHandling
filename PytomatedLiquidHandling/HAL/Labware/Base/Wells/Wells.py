from .Layout import AlphaNumeric, Numeric
from .Segment import Segment

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Wells:
    Layout: AlphaNumeric | Numeric
    SequencesPerWell: int
    MaxVolume: float
    DeadVolume: float
    Segments: list[Segment]
