from __future__ import annotations

from pydantic import dataclasses

from plh.implementation.tools import HALDevice

from .dimensions import Dimensions
from .layout import AlphanumericLayout, NumericLayout
from .transport_offsets import TransportOffsets


@dataclasses.dataclass(kw_only=True, eq=False)
class LabwareBase(HALDevice):
    """Type of physical labware (200uL plate, lid, etc.)."""

    dimensions: Dimensions
    """Dimensions object."""

    transport_offsets: TransportOffsets
    """Transport offsets object."""

    layout: AlphanumericLayout | NumericLayout
    """Layout object."""
