from __future__ import annotations

from pydantic import dataclasses

from ..layout import LayoutSorting, NumericLayout
from ..non_pipettable_labware import NonPipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVacuumManifoldShort(NonPipettableLabware):
    def __init__(
        self: HamiltonVacuumManifoldShort,
        identifier: str = "HamiltonVacuumManifoldShort",
    ):
        super().__init__(
            identifier=identifier,
            x_length=154,
            y_length=95,
            z_length=0,
            transport_open_offset=10,
            transport_close_offset=2,
            transport_top_offset=6,
            transport_bottom_offset=23,
            layout=NumericLayout(
                rows=1,
                columns=1,
                direction=LayoutSorting.Columnwise,
            ),
        )
