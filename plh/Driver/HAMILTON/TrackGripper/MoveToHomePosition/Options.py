from enum import Enum

import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    SpeedPercentage: int = 50
    CollisionControl: YesNoOptions = YesNoOptions.Yes
