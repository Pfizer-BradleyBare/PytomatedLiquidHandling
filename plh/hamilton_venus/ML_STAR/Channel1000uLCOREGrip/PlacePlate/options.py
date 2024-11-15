from pydantic import dataclasses

from plh.hamilton_venus.complex_inputs import XSpeedOptions
from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    EjectTool: bool
    XSpeed: XSpeedOptions = XSpeedOptions.XSpeed4
    ZSpeed: float = 128.7
    PressOnDistance: float = 1
    CheckPlateExists: bool = False
