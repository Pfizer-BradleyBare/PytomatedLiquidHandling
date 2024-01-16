from __future__ import annotations

from .dimensions import Dimensions
from .exceptions import LabwareNotEqualError, LabwareNotSupportedError
from .labware_base import LabwareBase
from .layout import AlphaNumericLayout, LayoutSorting, NumericLayout
from .non_pipettable_labware import NonPipettableLabware
from .pipettable_labware import PipettableLabware
from .well import Well
from .well_segment import WellSegment

__all__ = [
    "LabwareBase",
    "LabwareNotEqualError",
    "LabwareNotSupportedError",
    "LayoutSorting",
    "AlphaNumericLayout",
    "NumericLayout",
    "Dimensions",
    "NonPipettableLabware",
    "PipettableLabware",
    "Well",
    "WellSegment",
]

identifier = str
devices: dict[identifier, LabwareBase] = {}
