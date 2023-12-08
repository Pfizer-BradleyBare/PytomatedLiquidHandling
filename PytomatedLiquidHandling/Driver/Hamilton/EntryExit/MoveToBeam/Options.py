from pydantic import Field, dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    ModuleNumber: int = Field(ge=1, le=3)
    StackNumber: int = Field(ge=1, le=4)
    OffsetFromBeam: float
