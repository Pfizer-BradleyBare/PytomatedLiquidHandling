from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        HandleID: int,
        ShakingSpeed: int,
    ):
        self.HandleID: int = HandleID
        self.ShakingSpeed: int = ShakingSpeed
