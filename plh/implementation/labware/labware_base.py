from __future__ import annotations

from pydantic import dataclasses

from plh.implementation.tools import GenericResource

from .layout import AlphanumericLayout, NumericLayout


@dataclasses.dataclass(kw_only=True, eq=False)
class LabwareBase(GenericResource):
    """Type of physical labware (200uL plate, lid, etc.)."""

    x_length: float
    """Also known as length."""

    y_length: float
    """Also known as depth."""

    z_length: float
    """Also known as height."""

    transport_open_offset: float
    """How much the grippers will open before moving to labware. This offset is added to the size of the labware."""

    transport_close_offset: float
    """How much the grippers should close around the labware. This offset is subtracted from the size of the labware."""

    transport_top_offset: float
    """How far down from the top of the labware the gripper will grip."""

    transport_bottom_offset: float
    """How far up from the bottom of the labware the gripper will grip."""

    layout: AlphanumericLayout | NumericLayout
    """Layout object."""
