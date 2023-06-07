from ......Driver.Tools.AbstractClasses import OptionsABC
from .....LayoutItem import CoverablePosition, NonCoverablePosition
from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(OptionsABC):
    LayoutItemInstance: CoverablePosition | NonCoverablePosition
    Position: int
