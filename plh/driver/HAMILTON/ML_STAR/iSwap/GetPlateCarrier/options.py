from pydantic import dataclasses

from plh.driver.HAMILTON.complex_inputs import GripForceOptions, GripModeOptions
from plh.driver.tools import OptionsBase


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
