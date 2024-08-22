from __future__ import annotations

from pydantic import dataclasses

from ..layout import LayoutSorting, NumericLayout
from ..non_pipettable_labware import NonPipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class AgilentBlackLid(NonPipettableLabware):
    def __init__(self: AgilentBlackLid, identifier: str = "AgilentBlackLid"):
        super().__init__(
            identifier=identifier,
            x_length=127.5,
            y_length=85,
            z_length=0,
            transport_open_offset=5,
            transport_close_offset=2,
            transport_top_offset=4.5,
            transport_bottom_offset=4,
            layout=NumericLayout(
                rows=1,
                columns=1,
                direction=LayoutSorting.Columnwise,
            ),
        )
