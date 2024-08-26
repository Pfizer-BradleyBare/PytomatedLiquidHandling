from pydantic import dataclasses

from plh.device.hamilton_venus.complex_inputs import LockStateOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LockState: LockStateOptions
