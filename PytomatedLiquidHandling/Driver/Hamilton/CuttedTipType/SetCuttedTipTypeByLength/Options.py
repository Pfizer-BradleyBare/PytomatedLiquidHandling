from enum import Enum

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    class TipTypeOptions(Enum):
        uL300 = 0
        uL300Filter = 1
        uL1000 = 4
        uL1000Filter = 5
        uL50 = 22
        uL50Filter = 23

    def __init__(self, *, TipType: TipTypeOptions, CutLength: float):
        self.TipType: int = TipType.value
        self.CutLength: float = CutLength
