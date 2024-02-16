from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class ToolOrientationOptions(Enum):
    Landscape = 0
    Portrait = 1


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ToolOrientation: ToolOrientationOptions
