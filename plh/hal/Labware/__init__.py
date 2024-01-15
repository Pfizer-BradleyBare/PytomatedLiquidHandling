from __future__ import annotations

from .exceptions import LabwareNotEqualError, LabwareNotSupportedError
from .labware_base import LabwareBase
from .layout import AlphaNumericLayout, LayoutSorting, NumericLayout

__all__ = [
    "LabwareBase",
    "LabwareNotEqualError",
    "LabwareNotSupportedError",
    "LayoutSorting",
    "AlphaNumericLayout",
    "NumericLayout",
]

identifier = str
devices: dict[identifier, LabwareBase] = {}
