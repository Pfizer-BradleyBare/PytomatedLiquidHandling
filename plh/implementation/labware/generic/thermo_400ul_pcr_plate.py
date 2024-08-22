from __future__ import annotations

from pydantic import dataclasses

from ..layout import AlphanumericLayout, LayoutSorting
from ..pipettable_labware import CalibrationPoint, PipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class Thermo400uLPCRPlate(PipettableLabware):
    def __init__(self: Thermo400uLPCRPlate, identifier: str = "Thermo400uLPCRPlate"):
        super().__init__(
            identifier=identifier,
            x_length=123.25,
            y_length=84.75,
            z_length=0,
            transport_open_offset=10,
            transport_close_offset=2,
            transport_top_offset=10,
            transport_bottom_offset=5,
            layout=AlphanumericLayout(
                rows=8,
                columns=12,
                direction=LayoutSorting.Columnwise,
            ),
            positions_per_well=1,
            max_volume=400,
            dead_volume=10,
            calibration_curve=_create_cal_curve(),
        )


def _create_cal_curve() -> list[CalibrationPoint]:
    vols = [56.745, 510.705]
    heights = [3, 11]

    return [
        CalibrationPoint(volume=vol, height=height)
        for vol, height in zip(vols, heights)
    ]
