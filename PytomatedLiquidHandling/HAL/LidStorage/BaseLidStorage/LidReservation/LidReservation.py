from .....Tools.AbstractClasses import UniqueObjectABC
from ....LayoutItem import Lid
from dataclasses import dataclass


@dataclass
class LidReservation(UniqueObjectABC):
    LidInstance: Lid
