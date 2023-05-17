from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        HandleID: str,
        Temperature: float,
    ):
        self.HandleID: str = HandleID
        self.Temperature: float = Temperature
