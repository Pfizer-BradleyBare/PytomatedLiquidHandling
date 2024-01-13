from pydantic import dataclasses

from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC


@dataclasses.dataclass(kw_only=True)
class Plate(LayoutItemABC):
    Labware: Labware.PipettableLabware
