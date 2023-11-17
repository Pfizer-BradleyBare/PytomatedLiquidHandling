from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC
from .CoverableFilterPlate import CoverableFilterPlate
from .FilterPlate import FilterPlate


class FilterPlateStack(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
    FilterPlate: CoverableFilterPlate | FilterPlate
