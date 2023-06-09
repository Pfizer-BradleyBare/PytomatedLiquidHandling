from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import DeckLocation, Labware

from ....Tools.AbstractClasses import UniqueObjectABC


@dataclass
class LayoutItemABC(UniqueObjectABC):
    Sequence: str
    DeckLocationInstance: DeckLocation.BaseDeckLocation.DeckLocationABC
    LabwareInstance: Labware.BaseLabware.LabwareABC
