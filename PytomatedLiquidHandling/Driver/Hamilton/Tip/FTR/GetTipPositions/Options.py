from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        TipSequence: str,
        NumPositions: int,
    ):
        self.TipSequence: str = TipSequence
        self.NumPositions: int = NumPositions
