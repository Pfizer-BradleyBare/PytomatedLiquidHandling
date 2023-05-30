from ......Driver.Tools.AbstractClasses import OptionsABC
from .....LayoutItem.BaseLayoutItem import LayoutItemABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        SourceLayoutItem: LayoutItemABC,
        DestinationLayoutItem: LayoutItemABC,
    ):
        self.SourceLayoutItem: LayoutItemABC = SourceLayoutItem
        self.DestinationLayoutItem: LayoutItemABC = DestinationLayoutItem
