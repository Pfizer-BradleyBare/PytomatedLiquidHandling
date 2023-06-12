from abc import abstractmethod

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC
from ....Driver.Tools.AbstractClasses.Backend import BackendABC
from dataclasses import dataclass, field


@dataclass
class Tip(InterfaceABC, UniqueObjectABC):
    PickupSequence: str
    MaxVolume: float

    TipPositions: list[int] = field(init=False, default_factory=list)
    RemainingTips: int = field(init=False, default=0)

    @abstractmethod
    def Reload(
        self,
    ):
        ...

    @abstractmethod
    def UpdateTipPositions(
        self,
        *,
        NumTips: int,
    ):
        ...

    @abstractmethod
    def UpdateRemainingTips(
        self,
    ):
        ...
