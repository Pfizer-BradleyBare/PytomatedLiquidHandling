from pydantic import dataclasses

from plh.device.hamilton_venus.complex_inputs import GripForceOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    GripperLabwareID: str
    PlateLabwareID: str
    GripWidth: float
    OpenWidth: float
    GripHeight: float = 3
    GripForce: GripForceOptions = GripForceOptions.GripForce4
    GripSpeed: float = 277.8
    ZSpeed: float = 128.7
    CheckPlateExists: bool = False
