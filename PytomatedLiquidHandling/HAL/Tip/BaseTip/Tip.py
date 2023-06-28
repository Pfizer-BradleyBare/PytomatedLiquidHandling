from abc import abstractmethod
from dataclasses import dataclass, field

from ....Driver.Tools.AbstractClasses.Backend import BackendABC
from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class Tip(InterfaceABC, UniqueObjectABC):
    PickupSequence: str
    MaxVolume: float

    _RemainingTips: int = field(init=False, default=0)

    @abstractmethod
    def Reload(
        self,
    ):
        ...

    @abstractmethod
    def GetTipPositions(
        self,
        *,
        NumTips: int,
    ) -> list[int]:
        ...

    @property
    def RemainingTips(self) -> int:
        return self._RemainingTips

    @abstractmethod
    def _UpdateRemainingTips(
        self,
    ):
        ...
