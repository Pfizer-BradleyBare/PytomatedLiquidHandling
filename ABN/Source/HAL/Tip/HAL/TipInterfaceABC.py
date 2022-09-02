from abc import abstractmethod
from ....AbstractClasses import InterfaceABC


class TipInterfaceABC(InterfaceABC):
    @abstractmethod
    def HALFlipTubeToolPickup(self):
        raise NotImplementedError

    @abstractmethod
    def HALFlipTubeToolEject(self):
        raise NotImplementedError

    @abstractmethod
    def HALFlipTubeOpen(self):
        raise NotImplementedError

    @abstractmethod
    def HALFlipTubeClose(self):
        raise NotImplementedError
