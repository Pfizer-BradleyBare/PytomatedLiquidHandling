from enum import Enum

from pydantic import Field

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    class GripModeOptions(Enum):
        GripOnShortSide = 0
        GripOnLongSide = 1

    class MovementOptions(Enum):
        Simple = 0
        Complex = 1
        Taught = 2

    class LabwareOrientationOptions(Enum):
        PositiveYAxis = 1
        PositiveXAxis = 2
        NegativeXAxis = 3

    LabwareID: str
    LabwareWidth: float
    OpenWidth: float
    GripHeight: float = 3
    GripMode: GripModeOptions = GripModeOptions.GripOnShortSide
    LabwareOrientation: LabwareOrientationOptions = (
        LabwareOrientationOptions.PositiveYAxis
    )
    Movement: MovementOptions = MovementOptions.Simple
    RetractDistance: float = 0
    LiftupHeight: float = 0
    TaughtPathName: str
    CoordinatedMovement: bool = False
    GripForcePercentage: int = Field(ge=0, le=100, default=100)
    SpeedPercentage: int = Field(ge=0, le=100, default=50)
    CollisionControl: YesNoOptions = YesNoOptions.Yes
