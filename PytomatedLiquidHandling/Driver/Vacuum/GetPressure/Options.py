from ....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, PumpID: int):

        self.PumpID: int = PumpID
