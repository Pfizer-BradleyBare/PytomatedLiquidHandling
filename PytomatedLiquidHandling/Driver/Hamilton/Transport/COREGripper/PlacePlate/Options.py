from enum import Enum
from dataclasses import dataclass
from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    class XSpeedOptions(Enum):
        XSpeed1 = 1
        XSpeed2 = 2
        XSpeed3 = 3
        XSpeed4 = 4
        XSpeed5 = 5

    PlateSequence: str
    EjectTool: YesNoOptions = YesNoOptions.No
    XSpeed: XSpeedOptions = XSpeedOptions.XSpeed4
    ZSpeed: float = 128.7
    PressOnDistance: float = 1
    CheckPlateExists: YesNoOptions = YesNoOptions.No
