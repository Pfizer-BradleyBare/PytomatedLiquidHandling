from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        HandleID: int,
    ):
        self.HandleID: int = HandleID
