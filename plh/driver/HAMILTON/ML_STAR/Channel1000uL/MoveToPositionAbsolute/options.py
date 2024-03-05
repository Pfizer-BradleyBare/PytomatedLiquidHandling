from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class DirectionOptions(Enum):
    X = 0
    Y = 1
    Z = 2


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    Direction: DirectionOptions
    AbsolutePosition: float
