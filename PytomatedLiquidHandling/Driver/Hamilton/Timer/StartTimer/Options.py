from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        WaitTime: float,
    ):
        self.WaitTime: float = WaitTime
        self.ShowTimer: bool = True
        self.IsStoppable: bool = True
