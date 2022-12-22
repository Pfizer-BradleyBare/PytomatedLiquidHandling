from abc import ABC, abstractmethod
from typing import Callable


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(
        self,
        CallbackFunction: Callable[[object, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> object:
        ...

    @abstractmethod
    def Deinitialize(
        self,
        CallbackFunction: Callable[[object, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> object:
        ...
