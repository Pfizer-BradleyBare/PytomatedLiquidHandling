from __future__ import annotations

from pydantic import dataclasses

from ..layout import AlphanumericLayout, LayoutSorting
from ..pipettable_labware import CalibrationPoint, PipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class CorningCostar2000uLPCRPlate(PipettableLabware):
    def __init__(
        self: CorningCostar2000uLPCRPlate,
        identifier: str = "CorningCostar2000uLPCRPlate",
    ):
        super().__init__(
            identifier=identifier,
            x_length=124.50,
            y_length=82.5,
            z_length=0,
            transport_open_offset=10,
            transport_close_offset=2,
            transport_top_offset=33,
            transport_bottom_offset=10,
            layout=AlphanumericLayout(
                rows=8,
                columns=12,
                direction=LayoutSorting.Columnwise,
            ),
            positions_per_well=1,
            max_volume=2000,
            dead_volume=10,
            calibration_curve=_create_cal_curve(),
        )


def _create_cal_curve() -> list[CalibrationPoint]:
    vols = [134.0416, 2566.0416]
    heights = [4, 42]

    return [
        CalibrationPoint(volume=vol, height=height)
        for vol, height in zip(vols, heights)
    ]
