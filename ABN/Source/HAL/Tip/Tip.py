from enum import Enum
from ...AbstractClasses import ObjectABC


class TipTypes(Enum):
    NTR = "NTR"
    FTR = "FTR"


class Tip(ObjectABC):
    def __init__(
        self,
        Name: str,
        PickupSequence: str,
        Type: TipTypes,
        MaxVolume: float,
    ):
        self.Name: str = Name
        self.PickupSequence: str = PickupSequence
        self.Type: TipTypes = Type
        self.MaxVolume: float = MaxVolume

    def GetName(self) -> str:
        return self.Name

    def GetPickupSequence(self) -> str:
        return self.PickupSequence

    def GetType(self) -> TipTypes:
        return self.Type

    def GetMaxVolume(self) -> float:
        return self.MaxVolume


class TipFTR(Tip):
    def __init__(self, Name: str, PickupSequence: str, MaxVolume: float):
        Tip.__init__(self, Name, PickupSequence, TipTypes.FTR, MaxVolume)


class TipNTR(Tip):
    def __init__(
        self, Name: str, PickupSequence: str, NTRWasteSequence: str, MaxVolume: float
    ):
        Tip.__init__(self, Name, PickupSequence, TipTypes.NTR, MaxVolume)
        self.NTRWasteSequence: str = NTRWasteSequence

    def GetNTRWasteSequence(self) -> str:
        return self.NTRWasteSequence
