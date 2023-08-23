from dataclasses import dataclass
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject


@dataclass
class CarrierABC(HALObject):
    TrackStart: int
    TrackEnd: int
    NumLabwarePositions: int
    ImageFilename3D: str
    ImageFilename2D: str
