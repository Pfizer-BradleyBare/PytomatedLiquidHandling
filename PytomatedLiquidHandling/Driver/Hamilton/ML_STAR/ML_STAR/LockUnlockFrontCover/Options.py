from dataclasses import dataclass
from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    class LockStateOptions(Enum):
        Unlocked = 0
        Locked = 1

    LockState: LockStateOptions
