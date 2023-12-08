from enum import Enum

from pydantic import Field, dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    class PositionOptions(Enum):
        Bottom = "Bottom"
        Beam = "Beam"

    ModuleNumber: int = Field(ge=1, le=3)
    StackNumber: int = Field(ge=1, le=4)
    Position: PositionOptions
