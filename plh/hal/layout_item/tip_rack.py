from pydantic import dataclasses

from plh.hal import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class TipRack(LayoutItemBase):
    """A rack that can hold tips used for pipetting."""

    labware: labware.NonPipettableLabware
    """You should not pipette to/from a tip rack."""
