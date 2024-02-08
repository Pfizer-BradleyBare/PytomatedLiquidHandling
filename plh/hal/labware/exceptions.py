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

    labwares: tuple[LabwareBase, LabwareBase]
    """tuple of LabwareBase objects that are not equal"""
