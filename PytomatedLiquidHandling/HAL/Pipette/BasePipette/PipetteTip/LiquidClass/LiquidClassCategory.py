from ......Tools.AbstractClasses import ObjectABC, UniqueItemTrackerABC
from .LiquidClass import LiquidClass


class LiquidClassCategory(UniqueItemTrackerABC[LiquidClass], ObjectABC):
    def __init__(self, Name: str):
        UniqueItemTrackerABC.__init__(self)
        self.Name: str = Name

    def GetName(self) -> str:
        return self.Name
