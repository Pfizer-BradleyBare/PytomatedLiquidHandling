from pydantic import dataclasses

from .layout_item_base import *
from .plate import Plate


@dataclasses.dataclass(kw_only=True)
class FilterPlate(Plate):
    """A plate that contains a filter. Useful for vacuum and centrifuge filtrations."""
