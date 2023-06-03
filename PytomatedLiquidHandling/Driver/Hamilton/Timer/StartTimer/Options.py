from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self, *, WaitTime: float, ShowTimer: bool = True, IsStoppable: bool = True
    ):
        self.WaitTime: float = WaitTime
        self.ShowTimer: bool = ShowTimer
        self.IsStoppable: bool = IsStoppable
