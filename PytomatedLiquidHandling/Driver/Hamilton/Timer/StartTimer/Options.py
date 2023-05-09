from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        WaitTime: float,
    ):
        self.WaitTime: float = WaitTime
        self.ShowTimer: bool = True
        self.IsStoppable: bool = True
