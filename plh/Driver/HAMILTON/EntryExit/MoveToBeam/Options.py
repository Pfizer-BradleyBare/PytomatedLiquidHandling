import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    ModuleNumber: int
    StackNumber: int
    OffsetFromBeam: float
