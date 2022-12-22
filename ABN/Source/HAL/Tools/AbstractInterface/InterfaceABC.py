from abc import ABC, abstractmethod
from typing import Callable

from ....Driver.Tools import Command, CommandTracker


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def Deinitialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...
