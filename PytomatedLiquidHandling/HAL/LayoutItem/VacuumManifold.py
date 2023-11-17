from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC


class VacuumManifold(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
