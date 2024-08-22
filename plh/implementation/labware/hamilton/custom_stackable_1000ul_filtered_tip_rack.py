from __future__ import annotations

from pydantic import dataclasses

from ..layout import LayoutSorting, NumericLayout
from ..non_pipettable_labware import NonPipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class CustomStackable1000uLFilteredTipRack(NonPipettableLabware):
    def __init__(
        self: CustomStackable1000uLFilteredTipRack,
        identifier: str = "CustomStackable1000uLFilteredTipRack",
    ):
        super().__init__(
            identifier=identifier,
            x_length=124.75,
            y_length=82.75,
            z_length=0,
            transport_open_offset=10,
            transport_close_offset=2,
            transport_top_offset=64,
            transport_bottom_offset=51,
            layout=NumericLayout(
                rows=8,
                columns=12,
                direction=LayoutSorting.Columnwise,
            ),
        )
