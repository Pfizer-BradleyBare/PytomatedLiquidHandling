from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        HandleID: int,
        Temperature: float,
    ):
        self.HandleID: int = HandleID
        self.Temperature: float = Temperature
