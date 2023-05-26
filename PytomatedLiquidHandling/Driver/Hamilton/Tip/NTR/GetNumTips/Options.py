from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        TipSequence: str,
    ):
        self.TipSequence: str = TipSequence
