from abc import ABC, abstractmethod


class InterfaceABC(ABC):
    def __init__(self, CustomErrorHandling: bool):
        self.CustomErrorHandling: bool = CustomErrorHandling

    @abstractmethod
    def Initialize(self):
        ...

    @abstractmethod
    def Deinitialize(self):
        ...
