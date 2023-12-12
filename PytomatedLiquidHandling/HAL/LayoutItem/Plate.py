from PytomatedLiquidHandling.HAL import Labware

from .Base import LayoutItemABC

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Plate(LayoutItemABC):
    Labware: Labware.PipettableLabware
