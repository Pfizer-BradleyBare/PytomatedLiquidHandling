from .CoverablePlate import CoverablePlate
from .FilterPlate import FilterPlate

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class CoverableFilterPlate(FilterPlate, CoverablePlate):
    ...
