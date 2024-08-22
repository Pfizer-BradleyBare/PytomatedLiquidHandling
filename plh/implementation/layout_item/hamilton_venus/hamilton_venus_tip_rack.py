from pydantic import dataclasses

from ..tip_rack_base import TipRackBase
from .hamilton_venus_layout_item_base import HamiltonVenusLayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusTipRack(HamiltonVenusLayoutItemBase, TipRackBase): ...
