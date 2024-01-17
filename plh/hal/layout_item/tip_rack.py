from pydantic import dataclasses

from plh.hal import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True)
class TipRack(LayoutItemBase):
    labware: labware.NonPipettableLabware
