import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class PlateLockStateOptions(Enum):
    Unlocked = 0
    Locked = 1


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    HandleID: int
    PlateLockState: PlateLockStateOptions
