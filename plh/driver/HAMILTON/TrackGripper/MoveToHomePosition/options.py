import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    SpeedPercentage: int = 50
    CollisionControl: YesNoOptions = YesNoOptions.Yes