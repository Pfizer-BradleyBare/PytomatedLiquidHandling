from __future__ import annotations

from pydantic import dataclasses

from ..layout import LayoutSorting, NumericLayout
from ..non_pipettable_labware import NonPipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonNestedTipRack(NonPipettableLabware):
    def __init__(
        self: HamiltonNestedTipRack,
        identifier: str = "HamiltonNestedTipRack",
    ):
        super().__init__(
            identifier=identifier,
            x_length=120.5,
            y_length=78.5,
            z_length=0,
            transport_open_offset=10,
            transport_close_offset=2,
            transport_top_offset=21,
            transport_bottom_offset=42,
            layout=NumericLayout(
                rows=8,
                columns=12,
                direction=LayoutSorting.Columnwise,
            ),
        )
