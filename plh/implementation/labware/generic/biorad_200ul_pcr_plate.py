from __future__ import annotations

from pydantic import dataclasses

from ..layout import AlphanumericLayout, LayoutSorting
from ..pipettable_labware import CalibrationPoint, PipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class Biorad200uLPCRPlate(PipettableLabware):
    def __init__(self: Biorad200uLPCRPlate, identifier: str = "Biorad200uLPCRPlate"):
        super().__init__(
            identifier=identifier,
            x_length=124.5,
            y_length=82.5,
            z_length=0,
            transport_open_offset=10,
            transport_close_offset=2,
            transport_top_offset=9,
            transport_bottom_offset=6,
            layout=AlphanumericLayout(
                rows=8,
                columns=12,
                direction=LayoutSorting.Columnwise,
            ),
            positions_per_well=1,
            max_volume=200,
            dead_volume=10,
            calibration_curve=_create_cal_curve(),
        )


def _create_cal_curve() -> list[CalibrationPoint]:
    vols = [242.1231]
    heights = [14.68]

    return [
        CalibrationPoint(volume=vol, height=height)
        for vol, height in zip(vols, heights)
    ]
