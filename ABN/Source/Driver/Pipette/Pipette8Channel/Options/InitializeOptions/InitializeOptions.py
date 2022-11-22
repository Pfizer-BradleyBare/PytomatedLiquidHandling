from enum import Enum

from ......Tools.AbstractClasses import ObjectABC


class InitializeOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        Sequence: str,
        ChannelNumber: int,
        SequencePosition: int,
    ):
        self.Name: str = Name
        self.ChannelNumber: int = ChannelNumber
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

    def GetName(self) -> str:
        return self.Name
