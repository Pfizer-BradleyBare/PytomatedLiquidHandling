import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    WaitTime: float
    ShowTimer: bool = True
    IsStoppable: bool = True