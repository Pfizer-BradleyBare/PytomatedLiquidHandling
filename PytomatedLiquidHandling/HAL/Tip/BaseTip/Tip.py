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
        CustomErrorHandling: bool,
        PickupSequence: str,
        Type: TipTypes,
        MaxVolume: float,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        TipInterface.__init__(self, CustomErrorHandling)
        self.PickupSequence: str = PickupSequence
        self.Type: TipTypes = Type
        self.MaxVolume: float = MaxVolume
