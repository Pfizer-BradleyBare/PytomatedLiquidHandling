from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import DeckLocation, Labware
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject


@dataclass
class LayoutItemABC(HALObject):
    Sequence: str
    DeckLocationInstance: DeckLocation.Base.DeckLocationABC
    LabwareInstance: Labware.Base.LabwareABC
