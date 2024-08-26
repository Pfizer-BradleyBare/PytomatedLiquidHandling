from pydantic import dataclasses

from plh.device.hamilton_venus.complex_inputs import PositionOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ModuleNumber: int
    StackNumber: int
    Position: PositionOptions
