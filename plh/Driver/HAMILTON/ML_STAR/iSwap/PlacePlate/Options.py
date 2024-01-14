import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
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

    LabwareID: str
    Movement: MovementOptions = MovementOptions.Simple
    RetractDistance: float = 0
    LiftupHeight: float = 0
    LabwareOrientation: LabwareOrientationOptions = (
        LabwareOrientationOptions.NegativeYAxis
    )
    CollisionControl: YesNoOptions = YesNoOptions.Yes
