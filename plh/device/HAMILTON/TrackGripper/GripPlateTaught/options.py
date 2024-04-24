from pydantic import dataclasses

from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    OpenWidth: float
    TaughtPathName: str
    CoordinatedMovement: bool = False
    GripForcePercentage: int = 100
    SpeedPercentage: int = 50
    CollisionControl: bool = True
