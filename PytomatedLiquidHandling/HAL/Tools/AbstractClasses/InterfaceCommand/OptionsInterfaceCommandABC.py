from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class OptionsInterfaceCommandABC(ABC):
    @abstractmethod
    def __init__(self):
        raise Exception("This class is not meant to be instantiated.")

    @abstractmethod
    @staticmethod
    def Execute(InterfaceHandle, OptionsInstance):
        ...

    @abstractmethod
    @staticmethod
    def ExecutionTime(OptionsInstance) -> float:
        ...
