from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

ExecuteReturnType = TypeVar("ExecuteReturnType")


@dataclass
class OptionsInterfaceCommandABC(ABC, Generic[ExecuteReturnType]):
    @abstractmethod
    def __init__(self):
        raise Exception("This class is not meant to be instantiated.")

    @abstractmethod
    @staticmethod
    def Execute(InterfaceHandle, OptionsInstance) -> ExecuteReturnType:
        ...

    @abstractmethod
    @staticmethod
    def ExecutionTime(OptionsInstance) -> float:
        ...
