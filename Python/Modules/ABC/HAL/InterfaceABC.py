from abc import ABC, abstractmethod

# This is an abstract loader class for loading configuration files


class InterfaceABC(ABC):
    @abstractmethod
    def HALInitialize(self) -> dict:
        raise NotImplementedError
