from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class OptionsTrackerInterfaceCommandABC(ABC):
    @abstractmethod
    def __init__(self):
        raise Exception("This class is not meant to be instantiated.")

    @abstractmethod
    @staticmethod
    def Execute(InterfaceHandle, OptionsTrackerInstance):
        ...

    @abstractmethod
    @staticmethod
    def ExecutionTime(OptionsTrackerInstance) -> float:
        ...
