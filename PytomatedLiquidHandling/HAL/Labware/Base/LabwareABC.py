from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools import AbstractClasses

from .Dimensions.Dimensions import Dimensions
from .TransportOffsets import TransportOffsets


@dataclass
class LabwareNotSupportedError(BaseException):
    """HAL device does not support your Labware.
    This can be thrown for any LayoutItem inputs.

    Attributes:
    Labwares: List of LabwareABC objects that were not supported
    """

    Labwares: list["LabwareABC"]


@dataclass
class LabwareNotEqualError(BaseException):
    """Your two input Labwares are not equal.
    This can be thrown for any source and destination LayoutItem inputs.

    Attributes:
    Labware1: One of the labwares that failed the equality
    Labware2: The other labware that failed
    """

    Labware1: "LabwareABC"
    Labware2: "LabwareABC"


@dataclass
class LabwareABC(AbstractClasses.HALObject):
    ImageFilename: str
    Dimensions: Dimensions
    TransportOffsets: TransportOffsets
