import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    ModuleNumber: int
    StackNumber: int
    OffsetFromBeam: float
