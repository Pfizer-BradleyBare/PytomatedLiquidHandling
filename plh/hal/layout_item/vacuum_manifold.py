from pydantic import dataclasses

from plh.hal import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class VacuumManifold(LayoutItemBase):
    """A manifold that is used as part of vacuum operations."""

    labware: labware.NonPipettableLabware
    """You would pipette to/from the plate that sits atop a vacuum manifold. You would not pipette to/from a vacuum manifold."""
