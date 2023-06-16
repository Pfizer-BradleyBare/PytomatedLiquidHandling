from dataclasses import dataclass

from ......Driver.Tools.AbstractClasses import OptionsABC
from .....LayoutItem.BaseLayoutItem import LayoutItemABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    LayoutItemInstance: LayoutItemABC
