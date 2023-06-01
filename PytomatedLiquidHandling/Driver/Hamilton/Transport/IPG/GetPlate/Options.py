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

    class GripModeOptions(Enum):
        GripOnShortSide = 0
        GripOnLongSide = 1

    class MovementOptions(Enum):
        Simple = 0
        Complex = 1

    class LabwareOrientationOptions(Enum):
        NegativeYAxis = 1
        PositiveXAxis = 2
        PositiveYAxis = 3
        NegativeXAxis = 4

    def __init__(
        self,
        *,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
        GripHeight: float = 3,
        GripMode: GripModeOptions = GripModeOptions.GripOnShortSide,
        Movement: MovementOptions = MovementOptions.Simple,
        RetractDistance: float = 0,
        LiftupHeight: float = 0,
        LabwareOrientation: LabwareOrientationOptions = LabwareOrientationOptions.NegativeYAxis,
        GripForce: int = 4,
        Tolerance: float = 2,
        InverseGrip: YesNoOptions = YesNoOptions.No,
        CollisionControl: YesNoOptions = YesNoOptions.Yes,
    ):
        self.PlateSequence: str = PlateSequence

        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.GripHeight: float = GripHeight
        self.GripMode: int = GripMode.value

        self.Movement: int = Movement.value

        # Only matters if movement is 1
        self.RetractDistance: float = RetractDistance
        self.LiftupHeight: float = LiftupHeight
        self.LabwareOrientation: int = LabwareOrientation.value

        self.GripForce: int = GripForce
        self.Tolerance: float = Tolerance
        self.InverseGrip: int = InverseGrip.value
        self.CollisionControl: int = CollisionControl.value
