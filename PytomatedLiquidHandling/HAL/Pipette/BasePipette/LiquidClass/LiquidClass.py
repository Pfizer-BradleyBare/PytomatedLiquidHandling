from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class LiquidClass(UniqueObjectABC):
    MaxVolume: float
