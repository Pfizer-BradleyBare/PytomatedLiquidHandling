from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class TipTypeOptions(Enum):
    uL300 = 0
    uL300Filter = 1
    uL1000 = 4
    uL1000Filter = 5
    uL50 = 22
    uL50Filter = 23


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    TipType: TipTypeOptions
    CutLength: float
