from pydantic import dataclasses

from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    HandleID: int
    Temperature: float
