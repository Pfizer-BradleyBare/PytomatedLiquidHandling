from enum import Enum

from ......Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        SequencePosition: int,
    ):
        self.SequencePosition: int = SequencePosition
