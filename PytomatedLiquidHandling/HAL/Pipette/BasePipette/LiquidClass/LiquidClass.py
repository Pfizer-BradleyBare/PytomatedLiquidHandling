from .....Tools.AbstractClasses import UniqueObjectABC
from dataclasses import dataclass


@dataclass
class LiquidClass(UniqueObjectABC):
    MaxVolume: float
