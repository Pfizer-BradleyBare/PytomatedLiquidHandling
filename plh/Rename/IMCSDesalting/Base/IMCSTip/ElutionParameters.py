from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.BaseClasses import UniqueObjectABC


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
