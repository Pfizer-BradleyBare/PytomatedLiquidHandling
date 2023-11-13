from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC


class Plate(LayoutItemABC):
    Labware: Labware.PipettableLabware
