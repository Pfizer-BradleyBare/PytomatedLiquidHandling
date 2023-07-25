from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import (
    OptionsABC,
    OptionsTrackerABC,
)

InterfaceType = TypeVar("InterfaceType")
OptionsTrackerType = TypeVar("OptionsTrackerType", bound=OptionsTrackerABC)


@dataclass
class OptionsTrackerInterfaceABC(ABC, Generic[InterfaceType]):
    class Options(OptionsABC):
        ...

    class OptionsTracker(OptionsTrackerABC[Options]):
        ...

    @abstractmethod
    @staticmethod
    def Execute(InterfaceHandle: InterfaceType, OptionsTrackerInstance: OptionsTracker):
        ...

    @abstractmethod
    @staticmethod
    def ExecutionTime(
        InterfaceHandle: InterfaceType, OptionsTrackerInstance: OptionsTracker
    ):
        ...
