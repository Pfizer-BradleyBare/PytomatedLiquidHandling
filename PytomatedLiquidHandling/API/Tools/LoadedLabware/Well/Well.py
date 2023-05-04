from .....Tools.AbstractClasses import UniqueObjectABC


class Well(UniqueObjectABC):
    def __init__(self, WellNumber: int, Volume: float):
        UniqueObjectABC.__init__(self, WellNumber)
        self.Volume: float = Volume
