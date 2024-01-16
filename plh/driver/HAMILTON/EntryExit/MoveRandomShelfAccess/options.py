import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class PositionOptions(Enum):
    Bottom = "Bottom"
    Beam = "Beam"


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    ModuleNumber: int
    StackNumber: int
    Position: PositionOptions
