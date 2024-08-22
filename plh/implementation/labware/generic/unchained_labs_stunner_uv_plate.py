from __future__ import annotations

from pydantic import dataclasses

from ..layout import AlphanumericLayout, LayoutSorting
from ..pipettable_labware import CalibrationPoint, PipettableLabware


@dataclasses.dataclass(kw_only=True, eq=False)
class UnchainedLabsStunnerUVPlate(PipettableLabware):
    def __init__(
        self: UnchainedLabsStunnerUVPlate,
        identifier: str = "UnchainedLabsStunnerUVPlate",
    ):
        super().__init__(
            identifier=identifier,
            x_length=124.5,
            y_length=82,
            z_length=0,
            transport_open_offset=10,
            transport_close_offset=2,
            transport_top_offset=8,
            transport_bottom_offset=4,
            layout=AlphanumericLayout(
                rows=8,
                columns=12,
                direction=LayoutSorting.Columnwise,
            ),
            positions_per_well=1,
            max_volume=3,
            dead_volume=0,
            calibration_curve=_create_cal_curve(),
        )


def _create_cal_curve() -> list[CalibrationPoint]:
    vols = [0.0000942, 0.0340182, 0.0772432, 1.9683132, 5.0696632]
    heights = [0.001, 0.121, 0.251, 1.201, 1.901]

    return [
        CalibrationPoint(volume=vol, height=height)
        for vol, height in zip(vols, heights)
    ]
