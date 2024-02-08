from __future__ import annotations

from dataclasses import dataclass

from plh.hal.exceptions import HALError

from .labware_base import LabwareBase


@dataclass
class LabwareNotSupportedError(HALError):
    """HAL device does not support your Labware.
    This can be thrown for any LayoutItem inputs.
    """

    labwares: list[LabwareBase]
    """List of LabwareBase objects that were not supported"""


@dataclass
class LabwareNotEqualError(HALError):
    """Your two input Labwares are not equal.
    This can be thrown for any source and destination LayoutItem inputs.

    """

    labware1: LabwareBase
    """Labware 1 that failed the equality"""

    labware2: LabwareBase
    """Labware 2 that failed the equality"""
