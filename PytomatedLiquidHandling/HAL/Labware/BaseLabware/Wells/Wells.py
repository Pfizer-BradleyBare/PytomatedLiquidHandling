from .WellEquation.WellEquationTracker import WellEquationTracker
from dataclasses import dataclass


@dataclass
class Wells:
    Columns: int
    Rows: int
    SequencesPerWell: int
    MaxVolume: float
    WellDeadVolume: float
    WellEquationTrackerInstance: WellEquationTracker
