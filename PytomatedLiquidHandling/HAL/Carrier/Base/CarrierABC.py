from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from pydantic import dataclasses


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

    TrackStart: int
    TrackEnd: int
    NumLabwarePositions: int
    ImagePath3D: str
    ImagePath2D: str
