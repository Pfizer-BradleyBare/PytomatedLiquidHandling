from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import dataclasses

from plh.hal.tools import HALDevice

if TYPE_CHECKING:
    from .dimensions import Dimensions
    from .layout import AlphaNumericLayout, NumericLayout
    from .transport_offsets import TransportOffsets


@dataclasses.dataclass(kw_only=True)
class LabwareBase(HALDevice):
    image_filename: str
    part_number: str
    dimensions: Dimensions
    transport_offsets: TransportOffsets
    layout: AlphaNumericLayout | NumericLayout
