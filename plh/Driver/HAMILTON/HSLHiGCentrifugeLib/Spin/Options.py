import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    GForce: float
    AccelerationPercent: float
    DecelerationPercent: float
