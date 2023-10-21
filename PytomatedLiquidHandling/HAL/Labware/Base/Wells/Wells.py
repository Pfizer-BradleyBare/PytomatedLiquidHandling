from pydantic import BaseModel
from .Layout import AlphaNumeric, Numeric
from .Segment import Segment


class Wells(BaseModel):
    Layout: AlphaNumeric | Numeric
    SequencesPerWell: int
    MaxVolume: float
    DeadVolume: float
    Segments: list[Segment]
