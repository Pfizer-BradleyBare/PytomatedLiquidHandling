from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from .Interface.TipInterface import TipInterface


class TipTypes(Enum):
    NTR = "NTR"
    FTR = "FTR"
    FTRSlim = "FTRSlim"


class Tip(UniqueObjectABC, TipInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        PickupSequence: str,
        Type: TipTypes,
        MaxVolume: float,
    ):
        self.UniqueIdentifier: str = UniqueIdentifier
        self.PickupSequence: str = PickupSequence
        self.Type: TipTypes = Type
        self.MaxVolume: float = MaxVolume

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier
