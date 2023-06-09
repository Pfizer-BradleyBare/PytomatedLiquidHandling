from enum import Enum
from dataclasses import dataclass
from ....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    class TipTypeOptions(Enum):
        uL300 = 0
        uL300Filter = 1
        uL1000 = 4
        uL1000Filter = 5
        uL50 = 22
        uL50Filter = 23

    TipType: TipTypeOptions
    CutLength: float
