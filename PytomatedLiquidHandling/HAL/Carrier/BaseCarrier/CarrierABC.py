from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class CarrierABC(UniqueObjectABC):
    TrackStart: int
    TrackEnd: int
    NumLabwarePositions: int
    ImageFilename3D: str
    ImageFilename2D: str
