from .BaseLayoutItem import LayoutItemABC
from .Lid import Lid
from dataclasses import dataclass, field


@dataclass
class CoverablePosition(LayoutItemABC):
    LidInstance: Lid
    IsCovered: bool = field(init=False, default=False)

    def Cover(self):
        self.IsCovered = True

    def Uncover(self):
        self.IsCovered = False
