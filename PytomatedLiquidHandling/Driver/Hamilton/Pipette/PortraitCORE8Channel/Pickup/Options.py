from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        Sequence: str,
        ChannelNumber: int,
        SequencePosition: int,
    ):
        self.ChannelNumber: int = ChannelNumber
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition
