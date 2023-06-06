from ....Tools.AbstractClasses import UniqueObjectABC
from .Dimensions.Dimensions import Dimensions
from dataclasses import dataclass


@dataclass
class LabwareABC(UniqueObjectABC):
    DimensionsInstance: Dimensions
