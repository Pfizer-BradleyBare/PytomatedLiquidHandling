from enum import Enum

from ....Tools.BaseClasses import OptionsABC


class Options(OptionsABC):
    class ToolOrientationOptions(Enum):
        Landscape = 0
        Portrait = 1

    ToolOrientation: ToolOrientationOptions
