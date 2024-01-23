from __future__ import annotations

import pathlib

from pydantic import dataclasses, model_validator

from plh.hal.tools import HALDevice


@dataclasses.dataclass(kw_only=True)
class CarrierBase(HALDevice):
    """A physical carrier on an automation system deck.

    Attributes
    ----------
        TrackStart: The deck track where the carrier starts (Starting contact point).
        TrackEnd: The deck track where the carrier ends (Ending contact point).
        NumLabwarePositions: Number of labware supported by the carrier.
        ImagePath3D: Full path to a 3D model
        ImagePath2D: Full path to a 3D image
    """

    identifier: str = "None"

    track_start: int
    track_end: int
    num_labware_positions: int
    model_path_3d: pathlib.Path | None
    image_path_2d: pathlib.Path | None

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: CarrierBase) -> CarrierBase:
        if v.identifier == "None":
            v.identifier = f"Carrier{v.track_start}"
        return v
