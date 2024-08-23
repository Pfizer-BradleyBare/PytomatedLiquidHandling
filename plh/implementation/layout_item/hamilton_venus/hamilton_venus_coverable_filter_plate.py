from __future__ import annotations

from pydantic import dataclasses

from .hamilton_venus_coverable_plate import HamiltonVenusCoverablePlate
from .hamilton_venus_filter_plate import HamiltonVenusFilterPlate


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusCoverableFilterPlate(
    HamiltonVenusFilterPlate,
    HamiltonVenusCoverablePlate,
):
    """A coverable plate that contains a filter. Filter plates are always placed atop a collection plate. Useful for vacuum and centrifuge filtrations."""
