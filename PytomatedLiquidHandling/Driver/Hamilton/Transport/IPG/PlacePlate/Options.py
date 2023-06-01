from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

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
        Movement: MovementOptions = MovementOptions.Simple,
        RetractDistance: float = 0,
        LiftupHeight: float = 0,
        LabwareOrientation: LabwareOrientationOptions = LabwareOrientationOptions.NegativeYAxis,
        CollisionControl: YesNoOptions = YesNoOptions.Yes,
    ):
        self.PlateSequence: str = PlateSequence

        self.Movement: int = Movement.value

        # Only matters if movement is 1
        self.RetractDistance: float = RetractDistance
        self.LiftupHeight: float = LiftupHeight
        self.LabwareOrientation: int = LabwareOrientation.value

        self.CollisionControl: int = CollisionControl.value
