from enum import Enum

from pydantic import Field

from ....Tools.BaseClasses import OptionsABC


class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    SpeedPercentage: int = Field(ge=0, le=100, default=50)
    CollisionControl: YesNoOptions = YesNoOptions.Yes
