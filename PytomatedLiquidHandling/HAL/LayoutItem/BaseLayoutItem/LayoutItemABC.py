from ....Tools.AbstractClasses import UniqueObjectABC
from ...DeckLocation.BaseDeckLocation import DeckLocationABC
from ...Labware.BaseLabware import LabwareABC
from dataclasses import dataclass


@dataclass
class LayoutItemABC(UniqueObjectABC):
    Sequence: str
    DeckLocationInstance: DeckLocationABC
    LabwareInstance: LabwareABC
