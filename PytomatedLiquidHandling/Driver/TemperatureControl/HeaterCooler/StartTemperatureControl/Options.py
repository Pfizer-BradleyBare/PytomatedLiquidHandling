from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, HandleID: str, Temperature: float):

        self.HandleID: str = HandleID
        self.Temperature: float = Temperature
