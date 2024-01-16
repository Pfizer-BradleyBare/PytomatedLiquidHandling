import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    class ToolOrientationOptions(Enum):
        Landscape = 0
        Portrait = 1

    ToolOrientation: ToolOrientationOptions
