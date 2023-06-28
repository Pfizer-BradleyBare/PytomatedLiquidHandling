from dataclasses import dataclass

from ......Driver.Tools.AbstractClasses import OptionsABC
from .....LayoutItem import CoverableItem, NonCoverableItem


@dataclass(kw_only=True)
class Options(OptionsABC):
    LayoutItemInstance: CoverableItem | NonCoverableItem
    Position: int
