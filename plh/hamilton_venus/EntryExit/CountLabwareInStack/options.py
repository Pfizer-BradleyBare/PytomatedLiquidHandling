from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ModuleNumber: int
    StackNumber: int
    LabwareID: str
    IsNTRRack: bool
