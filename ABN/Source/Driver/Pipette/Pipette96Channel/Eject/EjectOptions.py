from enum import Enum

from .....Tools.AbstractClasses import ObjectABC


class EjectOptions(ObjectABC):
    def __init__(self, Name: str, Sequence: str, SequencePosition: int):
        self.Name: str = Name
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

    def GetName(self) -> str:
        return self.Name
