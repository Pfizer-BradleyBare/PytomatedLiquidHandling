from enum import Enum

import dataclasses

from .....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    class GripForceOptions(Enum):
        GripForce0 = 0
        GripForce1 = 1
        GripForce2 = 2
        GripForce3 = 3
        GripForce4 = 4
        GripForce5 = 5
        GripForce6 = 6
        GripForce7 = 7
        GripForce8 = 8
        GripForce9 = 9

    GripperLabwareID: str
    PlateLabwareID: str
    GripWidth: float
    OpenWidth: float
    GripHeight: float = 3
    GripForce: GripForceOptions = GripForceOptions.GripForce4
    GripSpeed: float = 277.8
    ZSpeed: float = 128.7
    CheckPlateExists: YesNoOptions = YesNoOptions.No
