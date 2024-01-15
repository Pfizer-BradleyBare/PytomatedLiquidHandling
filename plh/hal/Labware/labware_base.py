from pydantic import dataclasses

from plh.hal.tools import HALDevice

from .dimensions import Dimensions
from .TransportOffsets import TransportOffsets


@dataclasses.dataclass(kw_only=True)
class LabwareBase(HALDevice):
    image_filename: str
    part_number: str
    dimensions: Dimensions
    transport_offsets: TransportOffsets
