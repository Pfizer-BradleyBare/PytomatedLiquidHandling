from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class TipABC(InterfaceABC, HALObject):
    PickupSequence: str
    MaxVolume: float

    @dataclass(kw_only=True)
    class Options(OptionsABC):
        NumTips: int

    def Initialize(self):
        InterfaceABC.Initialize(self)
        self.TipCounterEdit()

    @abstractmethod
    def TipCounterEdit(self):
        ...

    @abstractmethod
    def GetTipPositions(self, OptionsInstance: Options) -> list[int]:
        ...

    @abstractmethod
    def GetRemainingTips(self) -> int:
        ...
