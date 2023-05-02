from abc import ABC
from typing import Self


class AdvancedOptionsABC(ABC):
    def UpdateOptions(self, AdvancedOptionsInstance: Self) -> Self:
        self.__dict__.update(AdvancedOptionsInstance.__dict__["UpdateItems"])
        # This is determined by the wrapper. If you forget the wrapper then you will get an error
        return self


class AdvancedSingleOptionsABC(AdvancedOptionsABC):
    def __init__(self, CustomErrorHandling: bool | None):
        self.CustomErrorHandling: bool | None = CustomErrorHandling


class AdvancedMultiOptionsABC(AdvancedOptionsABC):
    ...


class AdvancedMultiOptionsTrackerABC(AdvancedOptionsABC):
    def __init__(self, CustomErrorHandling: bool | None):
        self.CustomErrorHandling: bool | None = CustomErrorHandling
