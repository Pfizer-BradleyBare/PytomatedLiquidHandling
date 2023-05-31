from abc import abstractmethod

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC
from ....Driver.Tools.AbstractClasses.Backend import BackendABC


class Tip(UniqueObjectABC, InterfaceABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: BackendABC,
        CustomErrorHandling: bool,
        PickupSequence: str,
        MaxVolume: float,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        InterfaceABC.__init__(self, BackendInstance, CustomErrorHandling)
        self.PickupSequence: str = PickupSequence
        self.MaxVolume: float = MaxVolume

        self.TipPositions: list[int] = list()
        self.RemainingTips: int = 0

    def GetCurrentTipPositions(self) -> list[int]:
        if len(self.TipPositions) == 0:
            raise Exception("No tip positions are left. This should never happen...")

        return self.TipPositions

    def GetRemainingTips(self) -> int:
        return self.RemainingTips

    @abstractmethod
    def Reload(
        self,
    ):
        ...

    @abstractmethod
    def UpdateTipPositions(
        self,
        NumTips: int,
    ):
        ...

    @abstractmethod
    def UpdateRemainingTips(
        self,
    ):
        ...
