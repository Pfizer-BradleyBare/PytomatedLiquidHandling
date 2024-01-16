import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    class PositionOptions(Enum):
        Bottom = "Bottom"
        Beam = "Beam"

    ModuleNumber: int
    StackNumber: int
    Position: PositionOptions
