from enum import Enum

from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, Sequence: str, SequencePosition: int):

        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition
