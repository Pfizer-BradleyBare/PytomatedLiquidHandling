from __future__ import annotations

from pydantic import dataclasses

from plh.implementation.tools import HALDevice

from .layout import AlphanumericLayout, NumericLayout


@dataclasses.dataclass(kw_only=True, eq=False)
class LabwareBase(HALDevice):
    """Type of physical labware (200uL plate, lid, etc.)."""

    x_length: float
    """Also known as length."""

    y_length: float
    """Also known as depth."""

    z_length: float
    """Also known as height."""

    open: float
    """How much the grippers will open before moving to labware. This offset is added to the size of the labware."""

    close: float
    """How much the grippers should close around the labware. This offset is subtracted from the size of the labware."""

    top: float
    """How far down from the top of the labware the gripper will grip."""

    bottom: float
    """How far up from the bottom of the labware the gripper will grip."""

    layout: AlphanumericLayout | NumericLayout
    """Layout object."""
