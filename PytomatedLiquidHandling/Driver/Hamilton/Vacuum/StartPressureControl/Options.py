from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        PumpID: int,
        Pressure: float,
    ):
        self.PumpID: int = PumpID
        self.Pressure: float = Pressure
