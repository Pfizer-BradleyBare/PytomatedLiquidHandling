from pydantic import Field

from ....Tools.BaseClasses import OptionsABC


class Options(OptionsABC):
    ModuleNumber: int = Field(ge=1, le=3)
    StackNumber: int = Field(ge=1, le=4)
    OffsetFromBeam: float
