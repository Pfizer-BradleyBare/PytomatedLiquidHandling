from pydantic import dataclasses

from ..lid_base import LidBase
from .hamilton_venus_layout_item_base import HamiltonVenusLayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusLid(HamiltonVenusLayoutItemBase, LidBase): ...
