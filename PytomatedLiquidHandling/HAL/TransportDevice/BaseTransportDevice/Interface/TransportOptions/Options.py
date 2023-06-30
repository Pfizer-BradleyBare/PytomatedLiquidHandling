from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import LayoutItem

from ......Driver.Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    SourceLayoutItem: LayoutItem.BaseLayoutItem.LayoutItemABC
    DestinationLayoutItem: LayoutItem.BaseLayoutItem.LayoutItemABC
