from ......Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        HandleID: str,
    ):
        self.HandleID: str = HandleID
