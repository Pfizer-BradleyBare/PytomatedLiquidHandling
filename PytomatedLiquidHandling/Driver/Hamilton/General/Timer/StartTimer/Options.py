from .....Tools.BaseClasses import OptionsABC


class Options(OptionsABC):
    WaitTime: float
    ShowTimer: bool = True
    IsStoppable: bool = True
