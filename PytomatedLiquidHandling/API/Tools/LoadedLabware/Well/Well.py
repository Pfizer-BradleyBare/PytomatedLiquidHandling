from .....Tools.AbstractClasses import UniqueObjectABC


class Well(UniqueObjectABC):
    def __init__(self, WellNumber: int, Volume: float):
        self.WellNumber: int = WellNumber
        self.Volume: float = Volume

    def GetName(self) -> int:
        return self.WellNumber
