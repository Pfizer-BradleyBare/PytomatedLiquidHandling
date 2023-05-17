from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        SequencePosition: int,
    ):
        self.SequencePosition: int = SequencePosition
