from dataclasses import dataclass

from .WellEquation import WellEquation


@dataclass
class Wells:
    Columns: int
    Rows: int
    SequencesPerWell: int
    MaxVolume: float
    WellDeadVolume: float
    WellEquations: list[WellEquation]
