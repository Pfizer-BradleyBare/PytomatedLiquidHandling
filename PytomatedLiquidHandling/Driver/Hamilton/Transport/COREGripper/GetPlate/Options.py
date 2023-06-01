from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


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

    def __init__(
        self,
        *,
        GripperSequence: str,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
        GripHeight: float = 3,
        GripForce: GripForceOptions = GripForceOptions.GripForce4,
        GripSpeed: float = 277.8,
        ZSpeed: float = 128.7,
        CheckPlateExists: YesNoOptions = YesNoOptions.No,
    ):
        self.PlateSequence: str = PlateSequence
        self.GripperSequence: str = GripperSequence

        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.GripHeight: float = GripHeight
        self.GripForce: int = GripForce.value
        self.GripSpeed: float = GripSpeed
        self.ZSpeed: float = ZSpeed
        self.CheckPlateExists: int = CheckPlateExists.value
