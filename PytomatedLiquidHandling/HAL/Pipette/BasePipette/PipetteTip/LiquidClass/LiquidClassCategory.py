from ......Tools.AbstractClasses import UniqueObjectABC, UniqueObjectTrackerABC
from .LiquidClass import LiquidClass


class LiquidClassCategory(UniqueObjectTrackerABC[LiquidClass], UniqueObjectABC):
    def __init__(self, Name: str):
        UniqueObjectTrackerABC.__init__(self)
        self.Name: str = Name

    def GetName(self) -> str:
        return self.Name
