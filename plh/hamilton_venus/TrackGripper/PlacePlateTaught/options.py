from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    TaughtPathName: str
    ExtraOpenWidth: float = 6
    CoordinatedMovement: bool = False
    SpeedPercentage: int = 50
    CollisionControl: bool = True
