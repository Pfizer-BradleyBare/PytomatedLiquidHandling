from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import (
    InterfaceABC,
    InterfaceCommandABC,
    OptionsInterfaceCommandABC,
)


class TipCounterEditInterfaceCommand(InterfaceCommandABC[None]):
    ...


class GetTipPositionsInterfaceCommand(OptionsInterfaceCommandABC[list[int]]):
    @dataclass(kw_only=True)
    class Options(OptionsABC):
        NumTips: int


class GetRemainingTipsInterfaceCommand(InterfaceCommandABC[int]):
    ...


@dataclass
class Tip(InterfaceABC, UniqueObjectABC):
    PickupSequence: str
    MaxVolume: float
    TipCounterEdit: TipCounterEditInterfaceCommand = field(init=False)
    GetTipPositions: GetTipPositionsInterfaceCommand = field(init=False)
    GetRemainingTips: GetRemainingTipsInterfaceCommand = field(init=False)

    def _Initialize(self):
        InterfaceABC._Initialize(self)
        self._TipCounterEdit()

    @abstractmethod
    def _TipCounterEdit(self):
        ...

    @abstractmethod
    def _TipCounterEditTime(self) -> float:
        ...

    @abstractmethod
    def _GetTipPositions(
        self, OptionsInstance: GetTipPositionsInterfaceCommand.Options
    ) -> list[int]:
        ...

    @abstractmethod
    def _GetTipPositionsTime(
        self, OptionsInstance: GetTipPositionsInterfaceCommand.Options
    ) -> float:
        ...

    @abstractmethod
    def _GetRemainingTips(self) -> int:
        ...

    @abstractmethod
    def _GetRemainingTipsTime(self) -> float:
        ...

    def __post_init__(self):
        InterfaceABC.__post_init__(self)
        self.TipCounterEdit = TipCounterEditInterfaceCommand(
            self._TipCounterEdit, self._TipCounterEditTime
        )
        self.GetTipPositionsself = GetTipPositionsInterfaceCommand(
            self._GetTipPositions, self._GetTipPositionsTime
        )
        self.GetRemainingTips = GetRemainingTipsInterfaceCommand(
            self._GetRemainingTips, self._GetRemainingTipsTime
        )
