from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools import LabwareAddressing

from .WellEquation import WellEquation


@dataclass
class Wells:
    Addressing: LabwareAddressing.AlphaNumericAddressing | LabwareAddressing.NumericAddressing
    Columns: int
    Rows: int
    SequencesPerWell: int
    MaxVolume: float
    WellDeadVolume: float
    WellEquations: list[WellEquation]
