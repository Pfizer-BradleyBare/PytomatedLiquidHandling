from __future__ import annotations

from pydantic import Field, dataclasses, model_validator

from plh.hal.tools import HALDevice


@dataclasses.dataclass(kw_only=True)
class CarrierBase(HALDevice):
    """A physical carrier on an automation system deck.

    Attributes:
        TrackStart: The deck track where the carrier starts (Starting contact point).
        TrackEnd: The deck track where the carrier ends (Ending contact point).
        NumLabwarePositions: Number of labware supported by the carrier.
        ImagePath3D: Full path to a 3D model
        ImagePath2D: Full path to a 3D image
    """

    identifier: str = "None"

    track_start: int = Field(validation_alias="trackstart")
    track_end: int = Field(validation_alias="trackend")
    num_labware_positions: int = Field(validation_alias="numlabwarepositions")
    image_path_3d: str = Field(validation_alias="imagepath3d")
    image_path_2d: str = Field(validation_alias="imagepath2d")

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: CarrierBase) -> CarrierBase:
        if v.identifier == "None":
            v.identifier = f"Carrier{v.track_start}"
        return v
