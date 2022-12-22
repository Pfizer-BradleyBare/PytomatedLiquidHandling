from abc import abstractmethod
from typing import Callable

from .....Driver.Tools import Command, CommandTracker
from .....Tools.AbstractClasses import InterfaceABC


class TipInterface(InterfaceABC):
    def __init__(self):
        self.TipPosition: int = 0
        self.RemainingTips: int = 0

    def GetCurrentTipPosition(self) -> int:
        if self.TipPosition == 0:
            raise Exception("The tip position is zero. This should never happen...")

        return self.TipPosition

    def GetRemainingTips(self) -> int:
        return self.RemainingTips

    @abstractmethod
    def Reload(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateTipPosition(
        self,
        NumTips: int,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateRemainingTips(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...
