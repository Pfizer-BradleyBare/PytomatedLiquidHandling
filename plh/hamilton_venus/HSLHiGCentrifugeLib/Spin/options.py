from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    GForce: float
    AccelerationPercent: float
    DecelerationPercent: float
