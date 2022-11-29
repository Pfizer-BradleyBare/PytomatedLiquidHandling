from abc import ABC, abstractmethod

# This is an abstract loader class for loading configuration files


class ObjectABC(ABC):
    @abstractmethod
    def GetName(self) -> str | int:
        raise NotImplementedError  # this doesn't actually raise an error. This is an abstract method so python will complain
