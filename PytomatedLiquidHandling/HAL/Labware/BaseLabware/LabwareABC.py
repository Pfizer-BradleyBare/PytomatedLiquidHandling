from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets


@dataclass
class LabwareABC(UniqueObjectABC):
    ImageFilename: str
    DimensionsInstance: Dimensions
    TransportOffsetsInstance: TransportOffsets
