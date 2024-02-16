from pydantic import dataclasses

from plh.hal import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class Lid(LayoutItemBase):
    """A lid that can cover a layout item."""

    labware: labware.NonPipettableLabware
    """Lids can never be pipette to/from."""
