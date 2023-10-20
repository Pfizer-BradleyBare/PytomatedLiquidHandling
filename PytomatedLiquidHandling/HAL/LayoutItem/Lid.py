from .Base import LayoutItemABC
from PytomatedLiquidHandling.HAL import Labware


class Lid(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
