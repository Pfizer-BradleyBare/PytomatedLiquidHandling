from abc import ABC, abstractmethod
from ....Driver.Tools.AbstractOptions import AdvancedOptionsABC


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(
        self, AdvancedOptionsInstance: AdvancedOptionsABC = AdvancedOptionsABC()
    ):
        ...

    @abstractmethod
    def Deinitialize(
        self, AdvancedOptionsInstance: AdvancedOptionsABC = AdvancedOptionsABC()
    ):
        ...
