from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        HandleID: str,
    ):
        self.HandleID: str = HandleID
