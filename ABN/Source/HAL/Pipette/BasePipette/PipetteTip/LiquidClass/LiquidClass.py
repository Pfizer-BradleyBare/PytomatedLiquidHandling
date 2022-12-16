from ......Tools.AbstractClasses import ObjectABC


class LiquidClass(ObjectABC):
    def __init__(self, Name: str, MaxVolume: float):
        self.Name: str = Name
        self.MaxVolume: float = MaxVolume

    def GetName(self) -> str:
        return self.Name
