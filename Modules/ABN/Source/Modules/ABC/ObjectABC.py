from abc import ABC, abstractmethod

# This is an abstract loader class for loading configuration files


class ObjectABC(ABC):
    @abstractmethod
    def GetName(self) -> str:
        raise NotImplementedError
