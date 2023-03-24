from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, HandleID: int, ShakingSpeed: int):

        self.HandleID: int = HandleID
        self.ShakingSpeed: int = ShakingSpeed
