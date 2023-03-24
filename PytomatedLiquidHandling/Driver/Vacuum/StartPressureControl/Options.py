from ....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, PumpID: int, Pressure: float):

        self.PumpID: int = PumpID
        self.Pressure: float = Pressure
