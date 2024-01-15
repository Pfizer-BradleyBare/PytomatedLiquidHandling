from pydantic import dataclasses

from plh.hal import Labware

from .Base import LayoutItemBase


@dataclasses.dataclass(kw_only=True)
class TipRack(LayoutItemBase):
    Labware: Labware.NonPipettableLabware
