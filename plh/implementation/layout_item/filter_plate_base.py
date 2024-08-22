from pydantic import dataclasses

from .plate_base import PlateBase


@dataclasses.dataclass(kw_only=True, eq=False)
class FilterPlateBase(PlateBase):
    """A plate that contains a filter. Useful for vacuum and centrifuge filtrations."""
