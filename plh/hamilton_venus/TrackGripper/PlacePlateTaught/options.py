from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    OpenWidth: float
    TaughtPathName: str
    CoordinatedMovement: bool = False
    SpeedPercentage: int = 50
    CollisionControl: bool = True
