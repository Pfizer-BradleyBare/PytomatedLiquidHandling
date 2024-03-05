from pydantic import dataclasses

from plh.driver.HAMILTON.complex_inputs import LabwareOrientationOptions
from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    RetractDistance: float = 0
    LiftupHeight: float = 0
    LabwareOrientation: LabwareOrientationOptions = (
        LabwareOrientationOptions.NegativeYAxis
    )
    CollisionControl: bool = True
