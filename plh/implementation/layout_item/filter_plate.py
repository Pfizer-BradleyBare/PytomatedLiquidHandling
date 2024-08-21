from pydantic import dataclasses

from .plate import Plate


@dataclasses.dataclass(kw_only=True, eq=False)
class FilterPlate(Plate):
    """A plate that contains a filter. Useful for vacuum and centrifuge filtrations."""
