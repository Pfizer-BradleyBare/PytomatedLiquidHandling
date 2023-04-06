from enum import Enum

from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, Sequence: str, ChannelNumber: int, SequencePosition: int):

        self.ChannelNumber: int = ChannelNumber
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition
