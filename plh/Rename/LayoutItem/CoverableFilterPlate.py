from pydantic import dataclasses

from .CoverablePlate import CoverablePlate
from .FilterPlate import FilterPlate


@dataclasses.dataclass(kw_only=True)
class CoverableFilterPlate(FilterPlate, CoverablePlate):
    ...
