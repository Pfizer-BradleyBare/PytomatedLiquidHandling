from .Base import LayoutItemABC
from PytomatedLiquidHandling.HAL import Labware

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Lid(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
