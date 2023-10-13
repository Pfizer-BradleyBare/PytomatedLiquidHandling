from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets


@dataclass
class LabwareNotSupportedError(BaseException):
    Labwares: list["LabwareABC"]


@dataclass
class LabwareNotEqualError(BaseException):
    Labware1: "LabwareABC"
    Labware2: "LabwareABC"


@dataclass
class LabwareABC(HALObject):
    ImageFilename: str
    Dimensions: Dimensions
    TransportOffsets: TransportOffsets
