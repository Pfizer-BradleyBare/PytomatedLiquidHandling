from abc import ABC, abstractmethod
from typing import Callable

from ....Driver.Tools import Command, CommandTracker


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(
        self,
    ):
        ...

    @abstractmethod
    def Deinitialize(
        self,
    ):
        ...
