from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import LayoutItem


@dataclass(kw_only=True)
class Options(OptionsABC):
    LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    Position: int
