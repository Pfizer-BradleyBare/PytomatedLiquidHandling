from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC


class TipRack(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
