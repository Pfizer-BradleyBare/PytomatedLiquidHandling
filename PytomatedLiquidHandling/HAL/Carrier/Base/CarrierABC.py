from typing import Any, Optional, Self, cast

from pydantic import dataclasses, model_validator

from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice


@dataclasses.dataclass(kw_only=True)
class CarrierABC(HALDevice):
    """A physical carrier on an automation system deck.

    Attributes:
        TrackStart: The deck track where the carrier starts (Starting contact point).
        TrackEnd: The deck track where the carrier ends (Ending contact point).
        NumLabwarePositions: Number of labware supported by the carrier.
        ImagePath3D: Full path to a 3D model
        ImagePath2D: Full path to a 3D image
    """

    Identifier: str = "None"

    TrackStart: int
    TrackEnd: int
    NumLabwarePositions: int
    ImagePath3D: str
    ImagePath2D: str

    @model_validator(mode="after")
    def __ModelValidate(cls, v):
        if v.Identifier == "None":
            v.Identifier = f"Carrier{v.TrackStart}"
        return v
