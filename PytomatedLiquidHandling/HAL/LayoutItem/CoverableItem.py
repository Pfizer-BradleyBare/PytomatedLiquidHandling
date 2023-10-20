from PytomatedLiquidHandling.HAL import Labware
from pydantic import Field
from .Base import LayoutItemABC
from .Lid import Lid


class CoverableItem(LayoutItemABC):
    Labware: Labware.PipettableLabware
    Lid: Lid
    IsCovered: bool = Field(exclude=True, default=False)

    def Cover(self):
        self.IsCovered = True

    def Uncover(self):
        self.IsCovered = False
