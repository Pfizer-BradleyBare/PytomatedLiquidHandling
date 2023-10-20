from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC


class NonCoverableItem(LayoutItemABC):
    Labware: Labware.PipettableLabware
