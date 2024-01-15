from pydantic import dataclasses

from .coverable_plate import CoverablePlate
from .filter_plate import FilterPlate


@dataclasses.dataclass(kw_only=True)
class CoverableFilterPlate(FilterPlate, CoverablePlate):
    ...
