import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    class PlateLockStateOptions(Enum):
        Unlocked = 0
        Locked = 1

    HandleID: int
    PlateLockState: int
