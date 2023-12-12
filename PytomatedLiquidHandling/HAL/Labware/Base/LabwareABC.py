from PytomatedLiquidHandling.HAL.Tools import BaseClasses

from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class LabwareABC(BaseClasses.HALDevice):
    ImageFilename: str
    PartNumber: str
    Dimensions: Dimensions
    TransportOffsets: TransportOffsets
