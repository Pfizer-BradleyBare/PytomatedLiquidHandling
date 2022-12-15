from ......Tools.AbstractClasses import ObjectABC, TrackerABC
from .LiquidClass import LiquidClass


class LiquidClassCategory(TrackerABC[LiquidClass], ObjectABC):
    def __init__(self, Name: str):
        TrackerABC[LiquidClass].__init__(self)
        self.Name: str = Name

    def GetName(self) -> str:
        return self.Name
