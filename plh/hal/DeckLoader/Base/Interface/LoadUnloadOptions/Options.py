from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsBase
from PytomatedLiquidHandling.HAL import LayoutItem


@dataclass(kw_only=True)
class Options(OptionsBase):
    LayoutItemInstance: LayoutItem.Base.LayoutItemABC
