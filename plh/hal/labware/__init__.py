from __future__ import annotations

from .dimensions import Dimensions
from .labware_base import LabwareBase
from .layout import AlphanumericLayout, Layout, LayoutSorting, NumericLayout
from .non_pipettable_labware import NonPipettableLabware
from .pipettable_labware import PipettableLabware
from .pydantic_validators import validate_instance, validate_list
from .well import Well
from .well_segment import WellSegment

if True:
    from . import exceptions


__all__ = [
    "LabwareBase",
    "Dimensions",
    "Layout",
    "AlphanumericLayout",
    "NumericLayout",
    "LayoutSorting",
    "NonPipettableLabware",
    "PipettableLabware",
    "Well",
    "WellSegment",
    "exceptions",
    "validate_instance",
    "validate_list",
]

identifier = str
devices: dict[identifier, LabwareBase] = {}
