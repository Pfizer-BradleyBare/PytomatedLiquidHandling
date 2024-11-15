from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    WaitTime: float
    ShowTimer: bool = True
    IsStoppable: bool = True
