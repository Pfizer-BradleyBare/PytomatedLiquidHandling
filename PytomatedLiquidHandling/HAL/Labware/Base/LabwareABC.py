from PytomatedLiquidHandling.HAL.Tools import AbstractClasses

from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets


class LabwareABC(AbstractClasses.HALDevice):
    ImageFilename: str
    PartNumber: str
    Dimensions: Dimensions
    TransportOffsets: TransportOffsets
