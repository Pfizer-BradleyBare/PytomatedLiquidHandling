from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    TaughtPathName: str
    OpenWidth: float = 130
    GripHeight: float = 6
    CoordinatedMovement: bool = False
    GripForcePercentage: int = 100
    SpeedPercentage: int = 50
    CollisionControl: bool = True
