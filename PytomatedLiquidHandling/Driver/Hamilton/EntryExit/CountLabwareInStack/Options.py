from pydantic import Field

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    ModuleNumber: int = Field(ge=1, le=3)
    StackNumber: int = Field(ge=1, le=4)
    LabwareID: str
    IsNTRRack: bool
