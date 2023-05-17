from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        ComPort: int,
    ):
        self.ComPort: int = ComPort
