from abc import ABC, abstractmethod
from ....Driver.Tools.AbstractOptions import AdvancedSingleOptionsABC


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(
        self, *, AdvancedOptionsInstance: AdvancedSingleOptionsABC | None = None
    ):
        ...

    @abstractmethod
    def Deinitialize(
        self, *, AdvancedOptionsInstance: AdvancedSingleOptionsABC | None = None
    ):
        ...
