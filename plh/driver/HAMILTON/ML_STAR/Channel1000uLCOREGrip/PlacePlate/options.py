from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class XSpeedOptions(Enum):
    XSpeed1 = 1
    XSpeed2 = 2
    XSpeed3 = 3
    XSpeed4 = 4
    XSpeed5 = 5


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    EjectTool: bool
    XSpeed: XSpeedOptions = XSpeedOptions.XSpeed4
    ZSpeed: float = 128.7
    PressOnDistance: float = 1
    CheckPlateExists: bool = False
