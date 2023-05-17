from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        PumpID: int,
    ):
        self.PumpID: int = PumpID
