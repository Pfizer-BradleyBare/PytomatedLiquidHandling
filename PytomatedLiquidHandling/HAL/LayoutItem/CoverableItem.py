from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC
from .Lid import Lid


@dataclass
class CoverableItem(LayoutItemABC):
    Labware: Labware.PipettableLabware
    Lid: Lid
    IsCovered: bool = field(init=False, default=False)

    def Cover(self):
        self.IsCovered = True

    def Uncover(self):
        self.IsCovered = False
