from dataclasses import dataclass

from ....Tools.AbstractClasses import UniqueObjectABC
from .Dimensions.Dimensions import Dimensions


@dataclass
class LabwareABC(UniqueObjectABC):
    ImageFilename: str
    DimensionsInstance: Dimensions
