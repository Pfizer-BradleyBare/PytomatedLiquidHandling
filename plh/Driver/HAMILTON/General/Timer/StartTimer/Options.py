import dataclasses

from .....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    WaitTime: float
    ShowTimer: bool = True
    IsStoppable: bool = True
