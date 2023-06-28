from dataclasses import dataclass

from .....Tools.AbstractClasses import UniqueObjectABC
from ....LayoutItem.BaseLayoutItem import LayoutItemABC


@dataclass
class Reservation(UniqueObjectABC):
    LayoutItemInstance: LayoutItemABC
