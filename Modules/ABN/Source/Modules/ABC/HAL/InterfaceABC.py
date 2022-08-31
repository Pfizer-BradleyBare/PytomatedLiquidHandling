from abc import abstractmethod

# This is an abstract loader class for loading configuration files


class InterfaceABC:
    @abstractmethod
    def HALInitialize(self) -> dict:
        raise NotImplementedError
