from PytomatedLiquidHandling.HAL.DeckLocation import DeckLocation
from PytomatedLiquidHandling.HAL.Labware import NonPipettableLabware

from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....LayoutItem import Lid


class ReservableLid(Lid, NonUniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifer: str,
        Sequence: str,
        NonPipettableLabwareInstance: NonPipettableLabware,
        DeckLocationInstance: DeckLocation,
    ):
        Lid.__init__(
            self,
            UniqueIdentifer,
            Sequence,
            NonPipettableLabwareInstance,
            DeckLocationInstance,
        )
        NonUniqueObjectABC.__init__(self, "Reservable Lid")
