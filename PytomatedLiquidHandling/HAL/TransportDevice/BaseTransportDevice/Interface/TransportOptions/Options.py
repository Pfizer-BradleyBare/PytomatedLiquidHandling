from ......Driver.Tools.AbstractClasses import OptionsABC
from .....LayoutItem.BaseLayoutItem import LayoutItemABC
from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(OptionsABC):
    SourceLayoutItem: LayoutItemABC
    DestinationLayoutItem: LayoutItemABC
