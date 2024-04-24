from pydantic import dataclasses

from plh.device.HAMILTON.complex_inputs import (
    GripForceOptions,
    GripModeOptions,
    LabwareOrientationOptions,
)
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    GripWidth: float
    OpenWidth: float
    GripHeight: float = 3
    GripMode: GripModeOptions = GripModeOptions.GripOnShortSide
    RetractDistance: float = 0
    LiftupHeight: float = 0
    LabwareOrientation: LabwareOrientationOptions = (
        LabwareOrientationOptions.NegativeYAxis
    )
    GripForce: GripForceOptions = GripForceOptions.GripForce5
    Tolerance: float = 2
    InverseGrip: bool = False
    CollisionControl: bool = True
