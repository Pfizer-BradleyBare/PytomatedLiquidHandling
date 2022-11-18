from enum import Enum

from ......Tools.AbstractClasses import ObjectABC, OnOff


class TipOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        Sequence: str,
        NumTips: int,
    ):
        self.Name: str = Name
        self.Sequence: str = Sequence
        self.NumTips: int = NumTips

    def GetName(self) -> str:
        return self.Name
