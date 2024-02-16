from __future__ import annotations

from pydantic import FilePath, dataclasses

from plh.hal.tools import HALDevice

from .dimensions import Dimensions
from .layout import AlphanumericLayout, NumericLayout
from .transport_offsets import TransportOffsets


@dataclasses.dataclass(kw_only=True, eq=False)
class LabwareBase(HALDevice):
    """Type of physical labware (200uL plate, lid, etc.)."""

    part_number: str
    """Part number of the labware."""

    image_path_2d: FilePath | None
    """Full path to a 2D image."""

    image_path_3d: FilePath | None
    """Full path to a 3D image."""

    model_path_3d: FilePath | None
    """Full path to a 3D model."""

    container_image_path_2d: FilePath | None
    """Full path to a 2D image."""

    container_image_path_3d: FilePath | None
    """Full path to a 3D image."""

    container_model_path_3d: FilePath | None
    """Full path to a 3D model."""

    dimensions: Dimensions
    """Dimensions object."""

    transport_offsets: TransportOffsets
    """Transport offsets object."""

    layout: AlphanumericLayout | NumericLayout
    """Layout object."""
