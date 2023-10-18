from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC


@dataclass
class NonCoverableItem(LayoutItemABC):
    Labware: Labware.PipettableLabware
