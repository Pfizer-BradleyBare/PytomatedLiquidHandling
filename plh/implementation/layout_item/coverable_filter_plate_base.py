from pydantic import dataclasses

from .coverable_plate_base import CoverablePlateBase
from .filter_plate_base import FilterPlateBase


@dataclasses.dataclass(kw_only=True, eq=False)
class CoverableFilterPlateBaseBase(FilterPlateBase, CoverablePlateBase):
    """A coverable plate that contains a filter. Useful for vacuum and centrifuge filtrations."""
