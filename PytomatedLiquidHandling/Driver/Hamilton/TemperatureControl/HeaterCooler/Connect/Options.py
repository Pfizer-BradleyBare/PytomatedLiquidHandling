from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        ComPort: str,
    ):
        self.ComPort: str = ComPort
