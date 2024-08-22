from pydantic import dataclasses

from ..vacuum_manifold_base import VacuumManifoldBase
from .hamilton_venus_layout_item_base import HamiltonVenusLayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusVacuumManifold(HamiltonVenusLayoutItemBase, VacuumManifoldBase): ...
