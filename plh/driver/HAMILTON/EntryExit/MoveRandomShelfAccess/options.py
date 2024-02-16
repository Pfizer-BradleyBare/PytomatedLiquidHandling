from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class PositionOptions(Enum):
    Bottom = "Bottom"
    Beam = "Beam"


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ModuleNumber: int
    StackNumber: int
    Position: PositionOptions
