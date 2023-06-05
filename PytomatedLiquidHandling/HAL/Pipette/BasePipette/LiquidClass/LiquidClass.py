from .....Tools.AbstractClasses import UniqueObjectABC


class LiquidClass(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str, MaxVolume: float):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.MaxVolume: float = MaxVolume
