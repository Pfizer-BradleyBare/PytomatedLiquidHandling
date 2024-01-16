from __future__ import annotations

from dataclasses import dataclass

from .labware_base import LabwareBase


@dataclass
class LabwareNotSupportedError(BaseException):
    """HAL device does not support your Labware.
    This can be thrown for any LayoutItem inputs.

    Attributes
    ----------
    Labwares: List of LabwareBase objects that were not supported
    """

    labwares: list[LabwareBase]


@dataclass
class LabwareNotEqualError(BaseException):
    """Your two input Labwares are not equal.
    This can be thrown for any source and destination LayoutItem inputs.

    Attributes
    ----------
    Labware1: One of the labwares that failed the equality
    Labware2: The other labware that failed
    """

    labware1: LabwareBase
    labware2: LabwareBase
