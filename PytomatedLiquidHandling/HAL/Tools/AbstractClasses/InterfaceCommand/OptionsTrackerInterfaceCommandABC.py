from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

ExecuteReturnType = TypeVar("ExecuteReturnType")


@dataclass
class OptionsTrackerInterfaceCommandABC(ABC, Generic[ExecuteReturnType]):
    @abstractmethod
    def __init__(self):
        raise Exception("This class is not meant to be instantiated.")

    @abstractmethod
    @staticmethod
    def Execute(InterfaceHandle, OptionsTrackerInstance) -> ExecuteReturnType:
        ...

    @abstractmethod
    @staticmethod
    def ExecutionTime(OptionsTrackerInstance) -> float:
        ...
