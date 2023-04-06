from ....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, ComPort: int, PumpID: int):

        self.ComPort: int = ComPort
        self.PumpID: int = PumpID
