from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, ComPort: int):

        self.ComPort: int = ComPort
