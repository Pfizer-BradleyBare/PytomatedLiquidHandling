from ......Tools.AbstractClasses import UniqueObjectABC


class LiquidClass(UniqueObjectABC):
    def __init__(self, Name: str, MaxVolume: float):
        self.Name: str = Name
        self.MaxVolume: float = MaxVolume

    def GetName(self) -> str:
        return self.Name
