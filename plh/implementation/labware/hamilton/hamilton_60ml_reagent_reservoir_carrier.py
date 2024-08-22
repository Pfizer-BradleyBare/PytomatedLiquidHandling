from __future__ import annotations

from pydantic import dataclasses

from ..layout import LayoutSorting, NumericLayout
from ..pipettable_labware import CalibrationPoint, PipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class Hamilton60mLReagentReservoirCarrier(PipettableLabware):
    def __init__(
        self: Hamilton60mLReagentReservoirCarrier,
        identifier: str = "Hamilton60mLReagentReservoirCarrier",
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
                rows=5,
                columns=1,
                direction=LayoutSorting.Columnwise,
            ),
            positions_per_well=8,
            max_volume=60000,
            dead_volume=500,
            calibration_curve=_create_cal_curve(),
        )


def _create_cal_curve() -> list[CalibrationPoint]:
    vols = [
        3603.027,
        80009.43,
    ]
    heights = [
        6.72,
        62.72,
    ]

    return [
        CalibrationPoint(volume=vol, height=height)
        for vol, height in zip(vols, heights)
    ]
