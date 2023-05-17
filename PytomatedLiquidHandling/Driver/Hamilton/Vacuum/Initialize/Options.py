from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        ComPort: int,
        PumpID: int,
    ):
        self.ComPort: int = ComPort
        self.PumpID: int = PumpID
