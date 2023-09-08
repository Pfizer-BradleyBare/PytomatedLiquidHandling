from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets


@dataclass
class LabwareABC(HALObject):
    ImageFilename: str
    Dimensions: Dimensions
    TransportOffsets: TransportOffsets
