from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        ComPort: str,
    ):
        self.ComPort: str = ComPort
