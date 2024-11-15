from pydantic import dataclasses

from plh.hamilton_venus.complex_inputs import LockStateOptions
from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LockState: LockStateOptions
