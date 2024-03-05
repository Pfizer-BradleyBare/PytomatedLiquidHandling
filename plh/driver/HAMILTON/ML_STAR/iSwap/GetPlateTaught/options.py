from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


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


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    GripWidth: float
    OpenWidth: float
    TaughtPathName: str
    GripForce: int = 4
    Tolerance: float = 2
    CollisionControl: bool = True
