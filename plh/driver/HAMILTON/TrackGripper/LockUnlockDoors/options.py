from pydantic import dataclasses

from plh.driver.HAMILTON.complex_inputs import LockStateOptions
from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LockState: LockStateOptions
