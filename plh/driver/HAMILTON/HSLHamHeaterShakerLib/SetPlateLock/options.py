from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class PlateLockStateOptions(Enum):
    Unlocked = 0
    Locked = 1


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    HandleID: int
    PlateLockState: PlateLockStateOptions
