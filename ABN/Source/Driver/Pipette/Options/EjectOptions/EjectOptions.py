from enum import Enum

from .....Tools.AbstractClasses import ObjectABC


class EjectOptions(ObjectABC):
    def __init__(self, Name: str, Sequence: str, ChannelNumber: int):
        self.Name: str = Name
        self.ChannelNumber: int = ChannelNumber
        self.Sequence: str = Sequence

    def GetName(self) -> str:
        return self.Name
