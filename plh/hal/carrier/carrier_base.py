from __future__ import annotations

from pydantic import FilePath, dataclasses, model_validator

from plh.hal.tools import HALDevice


@dataclasses.dataclass(kw_only=True)
class CarrierBase(HALDevice):
    """A physical carrier on an automation system deck."""

    identifier: str = "None"
    """It is optional to specify an identifier. If one is not specified then the identifier will be ```Carrier_<track_start>```"""

    track_start: int
    """The deck track where the carrier starts (Starting contact point)."""

    track_end: int
    """The deck track where the carrier ends (Ending contact point)."""

    num_labware_positions: int
    """Number of labware supported by the carrier."""

    image_path_2d: FilePath | None
    """Full path to a 2D image."""

    model_path_3d: FilePath | None
    """Full path to a 3D model."""

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: CarrierBase) -> CarrierBase:
        if v.identifier == "None":
            v.identifier = f"Carrier{v.track_start}"
        return v
