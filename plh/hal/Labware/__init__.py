from __future__ import annotations

from .exceptions import LabwareNotEqualError, LabwareNotSupportedError
from .labware_base import LabwareBase

__all__ = ["LabwareBase", "LabwareNotEqualError", "LabwareNotSupportedError"]

identifier = str
devices: dict[identifier, LabwareBase] = {}
