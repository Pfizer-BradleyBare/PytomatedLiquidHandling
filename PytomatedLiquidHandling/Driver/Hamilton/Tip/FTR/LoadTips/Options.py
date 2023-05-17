from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        TipSequence: str,
    ):
        self.TipSequence: str = TipSequence

        self.LoadingText: str = "Load FTR Tips"
