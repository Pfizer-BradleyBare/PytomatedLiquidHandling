import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class LockStateOptions(Enum):
    Unlocked = 0
    Locked = 1


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LockState: LockStateOptions
