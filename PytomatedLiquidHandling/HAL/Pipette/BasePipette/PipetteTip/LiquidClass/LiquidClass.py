from ......Tools.AbstractClasses import UniqueObjectABC


class LiquidClass(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str, MaxVolume: float):
        self.UniqueIdentifier: str = UniqueIdentifier
        self.MaxVolume: float = MaxVolume

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier
