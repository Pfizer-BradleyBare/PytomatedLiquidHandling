import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class YesNoOptions(Enum):
    No = 0
    Yes = 1


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    SpeedPercentage: int = 50
    CollisionControl: YesNoOptions = YesNoOptions.Yes
