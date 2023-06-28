from dataclasses import dataclass, field

from .BaseLayoutItem import LayoutItemABC
from .Lid import Lid


@dataclass
class CoverableItem(LayoutItemABC):
    LidInstance: Lid
    IsCovered: bool = field(init=False, default=False)

    def Cover(self):
        self.IsCovered = True

    def Uncover(self):
        self.IsCovered = False
