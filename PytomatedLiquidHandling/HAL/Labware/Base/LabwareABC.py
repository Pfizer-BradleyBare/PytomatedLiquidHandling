from pydantic import dataclasses

from PytomatedLiquidHandling.HAL.Tools import BaseClasses

from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets


@dataclasses.dataclass(kw_only=True)
class LabwareABC(BaseClasses.HALDevice):
    ImageFilename: str
    PartNumber: str
    Dimensions: Dimensions
    TransportOffsets: TransportOffsets
