from dataclasses import dataclass

from ....Tools.AbstractClasses import UniqueObjectABC
from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets


@dataclass
class LabwareABC(UniqueObjectABC):
    ImageFilename: str
    DimensionsInstance: Dimensions
    TransportOffsetsInstance: TransportOffsets
