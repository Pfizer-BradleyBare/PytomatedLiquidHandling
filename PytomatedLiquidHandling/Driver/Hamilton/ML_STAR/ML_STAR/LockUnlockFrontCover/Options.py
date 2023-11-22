from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    class LockStateOptions(Enum):
        Unlocked = 0
        Locked = 1

    LockState: LockStateOptions
