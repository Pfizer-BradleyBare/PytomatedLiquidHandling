from enum import Enum

import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    class PositionOptions(Enum):
        Bottom = "Bottom"
        Beam = "Beam"

    ModuleNumber: int
    StackNumber: int
    Position: PositionOptions
