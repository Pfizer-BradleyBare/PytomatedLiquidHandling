from ......Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        TipSequence: str,
        NumPositions: int,
    ):
        self.TipSequence: str = TipSequence
        self.NumPositions: int = NumPositions
