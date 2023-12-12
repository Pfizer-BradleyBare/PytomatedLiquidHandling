from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC
from .CoverableFilterPlate import CoverableFilterPlate
from .FilterPlate import FilterPlate

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class FilterPlateStack(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
    FilterPlate: CoverableFilterPlate | FilterPlate
