from ......Tools.AbstractClasses import UniqueObjectABC, UniqueObjectTrackerABC
from .LiquidClass import LiquidClass


class LiquidClassCategory(UniqueObjectTrackerABC[LiquidClass], UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str):
        UniqueObjectTrackerABC.__init__(self)
        self.UniqueIdentifier: str = UniqueIdentifier

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier
