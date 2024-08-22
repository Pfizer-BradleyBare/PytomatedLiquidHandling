from pydantic import dataclasses

from ..plate_base import PlateBase
from .hamilton_venus_layout_item_base import HamiltonVenusLayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusPlate(HamiltonVenusLayoutItemBase, PlateBase): ...
