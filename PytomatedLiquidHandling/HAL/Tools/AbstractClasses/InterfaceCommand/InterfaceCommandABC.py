from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class InterfaceCommandABC(ABC):
    @abstractmethod
    def __init__(self):
        raise Exception("This class is not meant to be instantiated.")

    @abstractmethod
    @staticmethod
    def Execute(InterfaceHandle):
        ...

    @abstractmethod
    @staticmethod
    def ExecutionTime() -> float:
        ...
