from ....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, Sequence: str):

        self.Sequence: str = Sequence
