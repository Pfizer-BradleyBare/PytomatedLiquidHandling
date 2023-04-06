from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, TipSequence: str):

        self.TipSequence: str = TipSequence
