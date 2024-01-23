from __future__ import annotations

import pathlib

from pydantic import dataclasses

from plh.hal.tools import HALDevice

from .dimensions import Dimensions
from .layout import AlphanumericLayout, NumericLayout
from .transport_offsets import TransportOffsets


@dataclasses.dataclass(kw_only=True)
class LabwareBase(HALDevice):
    part_number: str
    model_path_3d: pathlib.Path | None
    image_path_2d: pathlib.Path | None
    dimensions: Dimensions
    transport_offsets: TransportOffsets
    layout: AlphanumericLayout | NumericLayout
