from __future__ import annotations

from pydantic import dataclasses

from plh.hal.tools import HALDevice

from .dimensions import Dimensions
from .layout import AlphanumericLayout, NumericLayout
from .transport_offsets import TransportOffsets


@dataclasses.dataclass(kw_only=True)
class LabwareBase(HALDevice):
    image_filename: str
    part_number: str
    dimensions: Dimensions
    transport_offsets: TransportOffsets
    layout: AlphanumericLayout | NumericLayout
