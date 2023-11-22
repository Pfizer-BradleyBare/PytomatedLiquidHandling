from enum import Enum

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    class PlateLockStateOptions(Enum):
        Unlocked = 0
        Locked = 1

    HandleID: int
    PlateLockState: int
