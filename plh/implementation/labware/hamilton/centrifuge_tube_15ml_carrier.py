from __future__ import annotations

from pydantic import dataclasses

from ..layout import LayoutSorting, NumericLayout
from ..pipettable_labware import CalibrationPoint, PipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class CentrifugeTube15mLCarrier(PipettableLabware):
    def __init__(
        self: CentrifugeTube15mLCarrier,
        identifier: str = "CentrifugeTube15mLCarrier",
    ):
        super().__init__(
            identifier=identifier,
            x_length=0,
            y_length=0,
            z_length=0,
            transport_open_offset=0,
            transport_close_offset=0,
            transport_top_offset=0,
            transport_bottom_offset=0,
            layout=NumericLayout(
                rows=24,
                columns=1,
                direction=LayoutSorting.Columnwise,
            ),
            positions_per_well=1,
            max_volume=15000,
            dead_volume=500,
            calibration_curve=_create_cal_curve(),
        )


def _create_cal_curve() -> list[CalibrationPoint]:
    vols = [
        1461.004,
        15269.62,
    ]
    heights = [
        23.36,
        118.61,
    ]

    return [
        CalibrationPoint(volume=vol, height=height)
        for vol, height in zip(vols, heights)
    ]
