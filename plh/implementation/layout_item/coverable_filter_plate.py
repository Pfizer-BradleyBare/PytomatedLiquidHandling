from pydantic import dataclasses

from .coverable_plate import CoverablePlate
from .filter_plate import FilterPlate


@dataclasses.dataclass(kw_only=True, eq=False)
class CoverableFilterPlate(FilterPlate, CoverablePlate):
    """A coverable plate that contains a filter. Useful for vacuum and centrifuge filtrations."""
