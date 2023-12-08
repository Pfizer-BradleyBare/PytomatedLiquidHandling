from enum import Enum

from pydantic import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    class LockStateOptions(Enum):
        Unlocked = 0
        Locked = 1

    LockState: LockStateOptions
