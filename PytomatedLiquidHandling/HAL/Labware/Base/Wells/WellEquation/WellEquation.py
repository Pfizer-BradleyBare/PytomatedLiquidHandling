from dataclasses import dataclass


@dataclass
class WellEquation:
    SegmentHeight: float
    SegmentEquation: str
