from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        HandleID: int,
        PlateLockState: int,
    ):
        self.HandleID: int = HandleID
        self.PlateLockState: int = PlateLockState
