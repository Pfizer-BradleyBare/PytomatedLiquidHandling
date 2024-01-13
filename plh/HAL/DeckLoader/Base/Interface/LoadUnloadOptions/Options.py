from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsABC
from PytomatedLiquidHandling.HAL import LayoutItem


@dataclass(kw_only=True)
class Options(OptionsABC):
    LayoutItemInstance: LayoutItem.Base.LayoutItemABC
