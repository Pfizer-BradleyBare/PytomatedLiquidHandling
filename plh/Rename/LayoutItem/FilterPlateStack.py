from pydantic import dataclasses

from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC
from .CoverableFilterPlate import CoverableFilterPlate
from .FilterPlate import FilterPlate


@dataclasses.dataclass(kw_only=True)
class FilterPlateStack(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
    FilterPlate: CoverableFilterPlate | FilterPlate
