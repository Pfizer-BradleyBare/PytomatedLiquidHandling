from enum import Enum

from pydantic import Field

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    class MovementOptions(Enum):
        Simple = 0
        Complex = 1
        Taught = 2

    class LabwareOrientationOptions(Enum):
        PositiveYAxis = 1
        PositiveXAxis = 2
        NegativeXAxis = 3

    LabwareID: str
    OpenWidth: float
    Movement: MovementOptions = MovementOptions.Simple
    RetractDistance: float = 0
    LiftupHeight: float = 0
    LabwareOrientation: LabwareOrientationOptions = (
        LabwareOrientationOptions.PositiveYAxis
    )
    TaughtPathName: str
    CoordinatedMovement: bool = False
    SpeedPercentage: int = Field(ge=0, le=100, default=50)
    CollisionControl: YesNoOptions = YesNoOptions.Yes
