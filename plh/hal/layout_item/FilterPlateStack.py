from pydantic import dataclasses

from plh.hal import Labware

from .Base import LayoutItemABC
from .CoverableFilterPlate import CoverableFilterPlate
from .FilterPlate import FilterPlate


@dataclasses.dataclass(kw_only=True)
class FilterPlateStack(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
    FilterPlate: CoverableFilterPlate | FilterPlate
