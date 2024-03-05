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


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    GripWidth: float
    OpenWidth: float
    GripHeight: float = 3
    GripMode: GripModeOptions = GripModeOptions.GripOnShortSide
    GripForce: GripForceOptions = GripForceOptions.GripForce5
    Tolerance: float = 2
    InverseGrip: bool = False
    CollisionControl: bool = True
