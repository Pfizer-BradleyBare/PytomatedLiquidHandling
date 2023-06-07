from .....Tools.AbstractClasses import UniqueObjectABC
from dataclasses import dataclass


@dataclass
class ElutionParameters(UniqueObjectABC):
    EquilibrationDispenseHeight: float
    SampleDispenseHeight: float
    ChaserDispenseHeight: float
    EquilibrationLoadVolume: float
    SampleLoadVolume: float
    ChaserLoadVolume: float
    EquilibrationDispenseVolume: float
    SampleDispenseVolume: float
    ChaserDispenseVolume: float
