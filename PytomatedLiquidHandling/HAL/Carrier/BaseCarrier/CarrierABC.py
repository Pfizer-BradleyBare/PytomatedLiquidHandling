from dataclasses import dataclass

from ....Tools.AbstractClasses import UniqueObjectABC


@dataclass
class CarrierABC(UniqueObjectABC):
    DeckLoaderUniqueIdentifier: str
    TrackStart: int
    TrackEnd: int
    NumLabwarePositions: int
    ImageFilename3D: str
    ImageFilename2D: str
